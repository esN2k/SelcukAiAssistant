# Benchmark Raporu (Ollama)

## Amaç
Yerel Ollama modellerinin Türkçe görevlerde hız/tepki metriklerinin karşılaştırılması yapılmıştır.

## Ortam
- Platform: Windows + Docker Desktop (Ollama konteyneri)
- Ollama URL: http://localhost:11435
- Veri seti: benchmark/data/selcuk_tr.jsonl

## Ayrıntılı Ölçüm (benchmark/run.py)
- max_new_tokens: 96
- temperature: 0.2
- max_samples: 6
- Not: Her model için aynı örnek sayısı kullanıldı.

| Model | Avg TTFT (ms) | Avg tok/s | Avg out tokens | Avg total time (s) |
| --- | --- | --- | --- | --- |
| ollama:aya:8b | 13392.93 | 3.33 | 36.8 | 18.786 |
| ollama:deepseek-r1:8b | 22835.77 | 4.68 | 96.0 | 22.836 |
| ollama:gemma2:2b | 4853.82 | 9.56 | 64.3 | 8.756 |
| ollama:llama3.1 | 12671.78 | 3.1 | 32.2 | 17.411 |
| ollama:llama3.2:3b | 6197.3 | 7.36 | 30.3 | 7.909 |
| ollama:mistral | 12323.86 | 4.04 | 66.7 | 21.916 |
| ollama:phi3:mini | 6772.77 | 8.26 | 86.8 | 13.155 |
| ollama:qwen2.5:7b | 11892.11 | 3.98 | 40.2 | 17.098 |
| ollama:selcuk_ai_assistant | 10186.69 | 3.49 | 34.0 | 15.138 |
| ollama:turkcell-llm-7b | 10126.57 | 4.1 | 33.3 | 14.166 |

## Hızlı Ölçüm (benchmark/ollama_quick.py)
- max_new_tokens: 48
- temperature: 0.2
- max_samples: 3

| Model | Koşum | Avg TTFT (ms) | Avg tok/s | Avg out tokens | Avg total time (s) |
| --- | --- | --- | --- | --- | --- |
| aya:8b | selcuk_tr_ollama_quick6 | 5137.96 | 3.12 | 34.7 | 10.814 |
| deepseek-r1:8b | selcuk_tr_qwen_deepseek | 20609.53 | 2.84 | 48.0 | 20.61 |
| gemma2:2b | selcuk_tr_ollama_quick6 | 10235.34 | 5.95 | 40.3 | 13.276 |
| llama3.2:3b | selcuk_tr_ollama_quick6 | 2451.41 | 7.19 | 37.3 | 5.192 |
| phi3:mini | selcuk_tr_ollama_quick6 | 13269.4 | 4.87 | 48.0 | 17.067 |
| qwen2.5:7b | selcuk_tr_qwen_deepseek | 22049.38 | 3.14 | 39.7 | 27.519 |
| selcuk_ai_assistant | selcuk_tr_ollama_quick6 | 4018.03 | 3.97 | 41.0 | 10.357 |
| turkcell-llm-7b | selcuk_tr_ollama_quick6 | 4523.9 | 3.68 | 42.3 | 11.516 |

## Kısa Yorum
- llama3.2:3b hız odaklı mod için güçlü bir adaydır (düşük TTFT ve yüksek tok/s).
- selcuk_ai_assistant ve turkcell-llm-7b benzer hız profiline sahiptir; kalite testleri ile birlikte seçilmelidir.
- qwen2.5:7b ve deepseek-r1:8b daha ağırdır; kalite odaklı senaryolarda değerlendirilmelidir.
- gemma2:2b ve phi3:mini düşük kaynak modları için uygundur.

## Sonuç Dosyaları
- benchmark/outputs/bench_ollama_*/summary.csv
- benchmark/outputs/selcuk_tr_ollama_quick6/summary.csv
- benchmark/outputs/selcuk_tr_qwen_deepseek/summary.csv
