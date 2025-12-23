import 'dart:async';

import 'package:flutter/material.dart';
import 'package:get/get.dart';
import 'package:selcukaiassistant/helper/pref.dart';
import 'package:selcukaiassistant/l10n/l10n.dart';
import 'package:selcukaiassistant/model/model_info.dart';
import 'package:selcukaiassistant/services/model_service.dart';
import 'package:selcukaiassistant/widget/model_card.dart';

class ModelPickerScreen extends StatefulWidget {
  const ModelPickerScreen({
    super.key,
    this.initialModels,
  });

  final List<ModelInfo>? initialModels;

  @override
  State<ModelPickerScreen> createState() => _ModelPickerScreenState();
}

class _ModelPickerScreenState extends State<ModelPickerScreen> {
  final TextEditingController _searchController = TextEditingController();
  List<ModelInfo> _models = [];
  bool _loading = true;

  @override
  void initState() {
    super.initState();
    _searchController.addListener(_onSearchChanged);
    unawaited(_loadModels());
  }

  @override
  void dispose() {
    _searchController
      ..removeListener(_onSearchChanged)
      ..dispose();
    super.dispose();
  }

  Future<void> _loadModels() async {
    final models = widget.initialModels ?? await ModelService.fetchModels();
    if (!mounted) {
      return;
    }
    setState(() {
      _models = models;
      _loading = false;
    });
  }

  void _onSearchChanged() {
    setState(() {});
  }

  List<ModelInfo> _filteredModels() {
    final query = _searchController.text.trim().toLowerCase();
    if (query.isEmpty) {
      return _models;
    }
    return _models.where((model) {
      return model.displayName.toLowerCase().contains(query) ||
          model.modelId.toLowerCase().contains(query) ||
          model.provider.toLowerCase().contains(query);
    }).toList();
  }

  void _selectModel(ModelInfo model) {
    Pref.selectedModel = model.id;
    Get.back<String>(result: model.id);
  }

  Widget _buildSection(
    BuildContext context,
    String title,
    List<ModelInfo> models,
    String selectedId,
  ) {
    if (models.isEmpty) {
      return const SizedBox.shrink();
    }
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Padding(
          padding: const EdgeInsets.only(top: 16, bottom: 8),
          child: Text(
            '$title (${models.length})',
            style: TextStyle(
              fontSize: 12,
              fontWeight: FontWeight.w600,
              color: Theme.of(context).colorScheme.primary,
            ),
          ),
        ),
        ...models.map(
          (model) => ModelCard(
            model: model,
            selected: model.id == selectedId,
            onSelect: model.available ? () => _selectModel(model) : null,
          ),
        ),
      ],
    );
  }

  @override
  Widget build(BuildContext context) {
    final l10n = context.l10n;
    final selectedId = Pref.selectedModel ?? '';
    final filtered = _filteredModels();
    final localModels = filtered.where((m) => m.isLocal).toList();
    final remoteModels = filtered.where((m) => m.isRemote).toList();

    return Scaffold(
      appBar: AppBar(
        title: Text(l10n.selectModelTitle),
      ),
      body: SafeArea(
        child: _loading
            ? const Center(child: CircularProgressIndicator())
            : Column(
                children: [
                  Padding(
                    padding: const EdgeInsets.all(12),
                    child: TextField(
                      controller: _searchController,
                      decoration: InputDecoration(
                        hintText: l10n.modelSearchHint,
                        prefixIcon: const Icon(Icons.search),
                        suffixIcon: _searchController.text.isNotEmpty
                            ? IconButton(
                                icon: const Icon(Icons.clear),
                                onPressed: _searchController.clear,
                              )
                            : null,
                        border: OutlineInputBorder(
                          borderRadius: BorderRadius.circular(12),
                        ),
                        contentPadding: const EdgeInsets.symmetric(
                          horizontal: 16,
                          vertical: 12,
                        ),
                      ),
                    ),
                  ),
                  Expanded(
                    child: filtered.isEmpty
                        ? Center(
                            child: Text(l10n.modelNoResults),
                          )
                        : RefreshIndicator(
                            onRefresh: _loadModels,
                            child: ListView(
                              padding: const EdgeInsets.symmetric(
                                horizontal: 12,
                                vertical: 8,
                              ),
                              children: [
                                _buildSection(
                                  context,
                                  l10n.modelLocalSection,
                                  localModels,
                                  selectedId,
                                ),
                                _buildSection(
                                  context,
                                  l10n.modelRemoteSection,
                                  remoteModels,
                                  selectedId,
                                ),
                              ],
                            ),
                          ),
                  ),
                ],
              ),
      ),
    );
  }
}
