"use strict";
(self["webpackChunkqslwidgets"] = self["webpackChunkqslwidgets"] || []).push([["lib_JupyterWidget_js"],{

/***/ "./lib/CommonWidget.js":
/*!*****************************!*\
  !*** ./lib/CommonWidget.js ***!
  \*****************************/
/***/ (function(__unused_webpack_module, exports, __webpack_require__) {


var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", ({ value: true }));
exports.defaultWidgetState = exports.CommonWidget = void 0;
const react_1 = __importDefault(__webpack_require__(/*! react */ "webpack/sharing/consume/default/react"));
const material_1 = __webpack_require__(/*! @mui/material */ "webpack/sharing/consume/default/@mui/material/@mui/material");
const react_image_labeler_1 = __webpack_require__(/*! react-image-labeler */ "webpack/sharing/consume/default/react-image-labeler/react-image-labeler");
const defaultWidgetState = {
    states: [],
    urls: [],
    type: "image",
    transitioning: false,
    config: { image: [], regions: [] },
    labels: { image: {}, polygons: [], masks: [], boxes: [] },
    action: "",
    preload: [],
    maxCanvasSize: 512,
    maxViewHeight: 512,
    buttons: {
        next: true,
        prev: true,
        save: true,
        config: true,
        delete: true,
        ignore: true,
        unignore: true,
    },
    base: {
        serverRoot: "",
        url: "",
    },
    progress: -1,
    mode: "light",
};
exports.defaultWidgetState = defaultWidgetState;
const CommonWidget = ({ extract }) => {
    var _a, _b;
    const config = extract("config");
    const states = extract("states");
    const transitioning = extract("transitioning");
    const urls = extract("urls");
    const type = extract("type");
    const labels = extract("labels");
    const action = extract("action");
    const progress = extract("progress");
    const mode = extract("mode");
    const buttons = extract("buttons");
    const preload = extract("preload");
    const maxCanvasSize = extract("maxCanvasSize");
    const maxViewHeight = extract("maxViewHeight");
    const common = {
        config: {
            image: ((_a = config.value) === null || _a === void 0 ? void 0 : _a.image) || [],
            regions: ((_b = config.value) === null || _b === void 0 ? void 0 : _b.regions) || [],
        },
        preload: preload.value,
        options: {
            progress: progress.value,
            maxCanvasSize: maxCanvasSize.value,
            showNavigation: true,
        },
        callbacks: {
            onSave: buttons.value.save
                ? (updated) => {
                    labels.set(updated);
                    action.set("save");
                }
                : undefined,
            onSaveConfig: buttons.value.config ? config.set : undefined,
            onNext: buttons.value.next ? () => action.set("next") : undefined,
            onPrev: buttons.value.prev ? () => action.set("prev") : undefined,
            onDelete: buttons.value.delete ? () => action.set("delete") : undefined,
            onIgnore: buttons.value.ignore ? () => action.set("ignore") : undefined,
            onUnignore: buttons.value.unignore
                ? () => action.set("unignore")
                : undefined,
        },
    };
    return (react_1.default.createElement(material_1.ThemeProvider, { theme: material_1.createTheme({
            palette: {
                mode: mode.value || "light",
            },
        }) },
        react_1.default.createElement(material_1.ScopedCssBaseline, null,
            react_1.default.createElement(material_1.Box, { style: { padding: 16 } },
                react_1.default.createElement(react_image_labeler_1.Labeler, null, states.value.length === 0 ? null : states.value.length == 1 ? (type.value === "image" ? (react_1.default.createElement(react_image_labeler_1.ImageLabeler, Object.assign({}, common, { maxViewHeight: maxViewHeight.value, labels: (labels.value || {}), target: urls.value[0], metadata: transitioning.value ? {} : states.value[0].metadata }))) : (react_1.default.createElement(react_image_labeler_1.VideoLabeler, Object.assign({}, common, { maxViewHeight: maxViewHeight.value, labels: (Array.isArray(labels.value)
                        ? labels.value
                        : []), target: urls.value[0], metadata: transitioning.value ? {} : states.value[0].metadata })))) : (react_1.default.createElement(react_image_labeler_1.BatchImageLabeler, Object.assign({}, common, { labels: (labels.value || {}), target: urls.value, states: transitioning.value ? [] : states.value, setStates: (newStates) => states.set(newStates) }))))))));
};
exports.CommonWidget = CommonWidget;
//# sourceMappingURL=CommonWidget.js.map

/***/ }),

/***/ "./lib/JupyterWidget.js":
/*!******************************!*\
  !*** ./lib/JupyterWidget.js ***!
  \******************************/
/***/ (function(__unused_webpack_module, exports, __webpack_require__) {


var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", ({ value: true }));
exports.MediaLabelerView = exports.MediaLabelerModel = void 0;
const react_1 = __importDefault(__webpack_require__(/*! react */ "webpack/sharing/consume/default/react"));
const react_dom_1 = __importDefault(__webpack_require__(/*! react-dom */ "webpack/sharing/consume/default/react-dom"));
const coreutils_1 = __webpack_require__(/*! @jupyterlab/coreutils */ "webpack/sharing/consume/default/@jupyterlab/coreutils");
const base_1 = __webpack_require__(/*! @jupyter-widgets/base */ "webpack/sharing/consume/default/@jupyter-widgets/base");
const hooks_1 = __webpack_require__(/*! ./hooks */ "./lib/hooks.js");
const CommonWidget_1 = __webpack_require__(/*! ./CommonWidget */ "./lib/CommonWidget.js");
const version_1 = __webpack_require__(/*! ./version */ "./lib/version.js");
const Widget = ({ model }) => {
    const extract = hooks_1.useModelStateExtractor(model);
    const base = extract("base");
    react_1.default.useEffect(() => {
        base.set({
            serverRoot: coreutils_1.PageConfig.getOption("serverRoot"),
            url: coreutils_1.PageConfig.getBaseUrl(),
        });
    });
    return react_1.default.createElement(CommonWidget_1.CommonWidget, { extract: extract });
};
class MediaLabelerModel extends base_1.DOMWidgetModel {
    defaults() {
        return Object.assign(Object.assign(Object.assign({}, super.defaults()), { _model_name: MediaLabelerModel.model_name, _model_module: MediaLabelerModel.model_module, _model_module_version: MediaLabelerModel.model_module_version, _view_name: MediaLabelerModel.view_name, _view_module: MediaLabelerModel.view_module, _view_module_version: MediaLabelerModel.view_module_version }), CommonWidget_1.defaultWidgetState);
    }
}
exports.MediaLabelerModel = MediaLabelerModel;
MediaLabelerModel.serializers = Object.assign({}, base_1.DOMWidgetModel.serializers);
MediaLabelerModel.model_name = "MediaLabelerModel";
MediaLabelerModel.model_module = version_1.MODULE_NAME;
MediaLabelerModel.model_module_version = version_1.MODULE_VERSION;
MediaLabelerModel.view_name = "MediaLabelerView"; // Set to null if no view
MediaLabelerModel.view_module = version_1.MODULE_NAME; // Set to null if no view
MediaLabelerModel.view_module_version = version_1.MODULE_VERSION;
class MediaLabelerView extends base_1.DOMWidgetView {
    render() {
        this.el.classList.add("qsl-image-labeler-widget");
        const component = react_1.default.createElement(Widget, {
            model: this.model,
        });
        react_dom_1.default.render(component, this.el);
    }
}
exports.MediaLabelerView = MediaLabelerView;
//# sourceMappingURL=JupyterWidget.js.map

/***/ }),

/***/ "./lib/hooks.js":
/*!**********************!*\
  !*** ./lib/hooks.js ***!
  \**********************/
/***/ (function(__unused_webpack_module, exports, __webpack_require__) {


var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", ({ value: true }));
exports.useModelEvent = exports.useModelState = exports.useModelStateExtractor = void 0;
const react_1 = __importDefault(__webpack_require__(/*! react */ "webpack/sharing/consume/default/react"));
/**
 *
 * @param name property name in the Python model object.
 * @returns model state and set state function.
 */
const useModelState = (name, model) => {
    const [value, setState] = react_1.default.useState(model === null || model === void 0 ? void 0 : model.get(name));
    useModelEvent(model, `change:${name}`, (model) => {
        setState(model.get(name));
    }, [name]);
    function set(val, options) {
        model === null || model === void 0 ? void 0 : model.set(name, val, options);
        model === null || model === void 0 ? void 0 : model.save_changes();
    }
    return { value, set };
};
exports.useModelState = useModelState;
const useModelStateExtractor = (model) => {
    return (name) => {
        return useModelState(name, model);
    };
};
exports.useModelStateExtractor = useModelStateExtractor;
/**
 * Subscribes a listener to the model event loop.
 * @param event String identifier of the event that will trigger the callback.
 * @param callback Action to perform when event happens.
 * @param deps Dependencies that should be kept up to date within the callback.
 */
const useModelEvent = (model, event, callback, deps) => {
    react_1.default.useEffect(() => {
        const callbackWrapper = (e) => model && callback(model, e);
        model === null || model === void 0 ? void 0 : model.on(event, callbackWrapper);
        return () => void (model === null || model === void 0 ? void 0 : model.unbind(event, callbackWrapper));
    }, (deps || []).concat([model]));
};
exports.useModelEvent = useModelEvent;
//# sourceMappingURL=hooks.js.map

/***/ }),

/***/ "./lib/version.js":
/*!************************!*\
  !*** ./lib/version.js ***!
  \************************/
/***/ ((__unused_webpack_module, exports, __webpack_require__) => {


// Copyright (c) Fausto Morales
// Distributed under the terms of the MIT License.
Object.defineProperty(exports, "__esModule", ({ value: true }));
exports.MODULE_NAME = exports.MODULE_VERSION = void 0;
// eslint-disable-next-line @typescript-eslint/ban-ts-comment
// @ts-ignore
// eslint-disable-next-line @typescript-eslint/no-var-requires
const data = __webpack_require__(/*! ../package.json */ "./package.json");
exports.MODULE_VERSION = data.version;
exports.MODULE_NAME = data.name;
//# sourceMappingURL=version.js.map

/***/ }),

/***/ "./package.json":
/*!**********************!*\
  !*** ./package.json ***!
  \**********************/
/***/ ((module) => {

module.exports = JSON.parse('{"name":"qslwidgets","version":"0.0.18","description":"Widgets for the QSL image labeling package.","keywords":["jupyter","jupyterlab","jupyterlab-extension","widgets"],"files":["lib/**/*.js","dist/*.js","css/*.css"],"homepage":"https://github.com/faustomorales/qsl","bugs":{"url":"https://github.com/faustomorales/qsl/issues"},"license":"MIT","author":{"name":"Fausto Morales","email":"fausto@robinbay.com"},"main":"lib/index.js","types":"./lib/index.d.ts","repository":{"type":"git","url":"https://github.com/faustomorales/qsl"},"scripts":{"build":"yarn run build:lib && yarn run build:nbextension && yarn run build:labextension:dev","build:prod":"yarn run build:lib && yarn run build:nbextension && yarn run build:labextension","build:labextension":"jupyter labextension build .","build:labextension:dev":"jupyter labextension build --development True .","build:lib":"tsc","build:nbextension":"webpack","clean":"yarn run clean:lib && yarn run clean:nbextension && yarn run clean:labextension","clean:lib":"rimraf lib","clean:labextension":"rimraf qsl/labextension","clean:nbextension":"rimraf qsl/nbextension/static/index.js","lint":"eslint . --ext .ts,.tsx --fix","lint:check":"eslint . --ext .ts,.tsx","format":"prettier --write src","prepack":"yarn run build:lib","test":"jest","watch":"npm-run-all -p watch:*","watch:lib":"tsc -w","watch:nbextension":"webpack --watch --mode=development","watch:labextension":"jupyter labextension watch ."},"dependencies":{"@emotion/react":"^11.8.1","@emotion/styled":"^11.8.1","@jupyter-widgets/base":"^1.1.10 || ^2.0.0 || ^3.0.0 || ^4.0.0","@mui/icons-material":"^5.6.1","@mui/material":"^5.6.1","react":"^17.0.2","react-dom":"^17.0.2","react-highlight":"^0.14.0","react-image-labeler":"0.0.1-alpha.53"},"devDependencies":{"@babel/core":"^7.5.0","@babel/preset-env":"^7.5.0","@babel/preset-react":"^7.14.5","@babel/preset-typescript":"^7.14.5","@jupyterlab/builder":"^3.0.0","@phosphor/application":"^1.6.0","@phosphor/widgets":"^1.6.0","@types/jest":"^26.0.0","@types/react":"^17.0.11","@types/react-dom":"^17.0.8","@types/react-highlight":"^0.12.5","@types/webpack-env":"^1.13.6","@typescript-eslint/eslint-plugin":"^3.6.0","@typescript-eslint/parser":"^3.6.0","acorn":"^7.2.0","babel-loader":"^8.2.2","css-loader":"^6.7.1","eslint":"^7.4.0","eslint-config-prettier":"^6.11.0","eslint-plugin-prettier":"^3.1.4","fs-extra":"^7.0.0","html-webpack-plugin":"^5.5.0","identity-obj-proxy":"^3.0.0","jest":"^26.0.0","mkdirp":"^0.5.1","npm-run-all":"^4.1.3","prettier":"^2.0.5","rimraf":"^2.6.2","source-map-loader":"^1.1.3","ts-jest":"^26.0.0","ts-loader":"^8.0.0","typescript":"~4.1.3","webpack":"^5.0.0","webpack-cli":"^4.0.0"},"babel":{"presets":["@babel/preset-env","@babel/preset-react","@babel/preset-typescript"]},"jupyterlab":{"extension":"lib/plugin","outputDir":"../qsl/ui/labextension/","sharedPackages":{"@jupyter-widgets/base":{"bundled":false,"singleton":true}}}}');

/***/ })

}]);
//# sourceMappingURL=lib_JupyterWidget_js.22d878849d6fed8b4310.js.map