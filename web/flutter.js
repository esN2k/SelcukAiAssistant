/**
 * flutter.js - Bootstraps the Flutter Web App
 * Restored by AI Assistant
 */
(function () {
  "use strict";

  var _flutter = window._flutter || {};
  window._flutter = _flutter;

  _flutter.loader = _flutter.loader || {};

  // Promise that resolves when main.dart.js calls didCreateEngineInitializer
  let engineInitializerResolver;
  const engineInitializerPromise = new Promise((resolve) => {
    engineInitializerResolver = resolve;
  });

  _flutter.loader.didCreateEngineInitializer = function (engineInitializer) {
    if (typeof engineInitializerResolver === "function") {
      engineInitializerResolver(engineInitializer);
    }
  };

  /**
   * Minimal implementation of FlutterLoader
   */
  class FlutterLoader {
    /**
     * Loads the main.dart.js entrypoint.
     * @param {*} options
     * @returns {Promise} that resolves to the EngineInitializer
     */
    async loadEntrypoint(options) {
      const { serviceWorker, ...entrypointOptions } = options || {};

      // 1. In a full implementation, we would register the service worker here.
      // For now, we skip it since serviceWorkerVersion is likely null or dev.

      // 2. Load main.dart.js
      const script = document.createElement("script");
      script.src = "main.dart.js";
      script.type = "application/javascript";
      document.body.appendChild(script);

      // 3. Wait for the engine initializer
      return engineInitializerPromise;
    }
  }

  // Expose the loader on _flutter for main.dart.js to find
  const loader = new FlutterLoader();
  _flutter.loader.loadEntrypoint = loader.loadEntrypoint.bind(loader);

  // Expose the Flutter object expected by index.html
  window.Flutter = {
    initializeApp: async function (options) {
      // 1. Load entrypoint
      const engineInitializer = await loader.loadEntrypoint(options);
      
      // 2. Initialize engine
      const appRunner = await engineInitializer.initializeEngine(options);
      
      // 3. Run app
      await appRunner.runApp();
    }
  };
})();
