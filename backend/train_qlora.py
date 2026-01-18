"""QLoRA training script for Selcuk University domain adaptation."""
from __future__ import annotations

import argparse
import logging
from typing import Any, Optional

import torch
from datasets import load_dataset
from peft import LoraConfig, get_peft_model, prepare_model_for_kbit_training
from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    BitsAndBytesConfig,
    DataCollatorForLanguageModeling,
    TrainingArguments,
    Trainer,
)

logger = logging.getLogger(__name__)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Train QLoRA adapter")
    parser.add_argument("--model-id", default="Turkcell/Turkcell-LLM-7b-v1")
    parser.add_argument("--data", default="data/selcuk_qa_dataset.jsonl")
    parser.add_argument("--output-dir", default="output/selcuk-qlora")
    parser.add_argument("--max-seq-len", type=int, default=2048)
    parser.add_argument("--epochs", type=int, default=3)
    parser.add_argument("--batch-size", type=int, default=2)
    parser.add_argument("--grad-accum", type=int, default=8)
    parser.add_argument("--learning-rate", type=float, default=2e-4)
    parser.add_argument("--lora-r", type=int, default=16)
    parser.add_argument("--lora-alpha", type=int, default=32)
    parser.add_argument("--lora-dropout", type=float, default=0.05)
    parser.add_argument(
        "--target-modules",
        default="q_proj,k_proj,v_proj,o_proj",
        help="Comma-separated module names for LoRA.",
    )
    return parser.parse_args()


def format_messages(messages: list[dict[str, Any]], tokenizer) -> Optional[str]:
    if not messages:
        return None
    if hasattr(tokenizer, "apply_chat_template"):
        try:
            return tokenizer.apply_chat_template(
                messages,
                tokenize=False,
                add_generation_prompt=False,
            )
        except Exception:
            pass
    lines = [f"{m.get('role', 'user')}: {m.get('content', '')}" for m in messages]
    return "\n".join(lines).strip()


def format_instruction(example: dict[str, Any]) -> Optional[str]:
    instruction = str(example.get("instruction", "")).strip()
    output = str(example.get("output", "")).strip()
    if not instruction or not output:
        return None
    input_text = str(example.get("input", "")).strip()
    if input_text:
        return (
            "### Talimat:\n"
            f"{instruction}\n\n"
            "### Girdi:\n"
            f"{input_text}\n\n"
            "### Cevap:\n"
            f"{output}"
        )
    return (
        "### Talimat:\n"
        f"{instruction}\n\n"
        "### Cevap:\n"
        f"{output}"
    )


def format_example(example: dict[str, Any], tokenizer) -> Optional[str]:
    if "messages" in example and isinstance(example["messages"], list):
        return format_messages(example["messages"], tokenizer)
    if "instruction" in example:
        return format_instruction(example)
    if "prompt" in example and "response" in example:
        prompt = str(example.get("prompt", "")).strip()
        response = str(example.get("response", "")).strip()
        if prompt and response:
            return f"{prompt}\n{response}"
    return None


def main() -> None:
    logging.basicConfig(level=logging.INFO)
    args = parse_args()

    bnb_config = BitsAndBytesConfig(
        load_in_4bit=True,
        bnb_4bit_quant_type="nf4",
        bnb_4bit_compute_dtype=torch.float16,
        bnb_4bit_use_double_quant=True,
    )

    tokenizer = AutoTokenizer.from_pretrained(args.model_id, use_fast=True)
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token

    model = AutoModelForCausalLM.from_pretrained(
        args.model_id,
        quantization_config=bnb_config,
        device_map="auto",
    )
    model = prepare_model_for_kbit_training(model)

    target_modules = [name.strip() for name in args.target_modules.split(",") if name]
    lora_config = LoraConfig(
        r=args.lora_r,
        lora_alpha=args.lora_alpha,
        target_modules=target_modules,
        lora_dropout=args.lora_dropout,
        bias="none",
        task_type="CAUSAL_LM",
    )
    model = get_peft_model(model, lora_config)
    model.print_trainable_parameters()

    dataset = load_dataset("json", data_files=args.data, split="train")

    def preprocess(example: dict[str, Any]) -> dict[str, Any]:
        text = format_example(example, tokenizer)
        if not text:
            return {}
        tokens = tokenizer(
            text,
            truncation=True,
            max_length=args.max_seq_len,
            padding="max_length",
        )
        tokens["labels"] = tokens["input_ids"].copy()
        return tokens

    dataset = dataset.map(preprocess, remove_columns=dataset.column_names)
    dataset = dataset.filter(lambda x: "input_ids" in x and len(x["input_ids"]) > 0)

    data_collator = DataCollatorForLanguageModeling(tokenizer=tokenizer, mlm=False)

    training_args = TrainingArguments(
        output_dir=args.output_dir,
        per_device_train_batch_size=args.batch_size,
        gradient_accumulation_steps=args.grad_accum,
        num_train_epochs=args.epochs,
        learning_rate=args.learning_rate,
        fp16=True,
        logging_steps=10,
        save_strategy="epoch",
        report_to="none",
    )

    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=dataset,
        tokenizer=tokenizer,
        data_collator=data_collator,
    )

    logger.info("Starting QLoRA training...")
    trainer.train()
    model.save_pretrained(args.output_dir)
    tokenizer.save_pretrained(args.output_dir)
    logger.info("Adapter saved to %s", args.output_dir)


if __name__ == "__main__":
    main()
