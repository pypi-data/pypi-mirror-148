"use strict";
(self["webpackChunkgosling_widget"] = self["webpackChunkgosling_widget"] || []).push([[345],{

/***/ 8138:
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony import */ var _widget_js__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(5203);
/* harmony import */ var higlass_dist_hglib_css__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(5995);



const style = document.createElement('style');
style.textContent = higlass_dist_hglib_css__WEBPACK_IMPORTED_MODULE_1__/* ["default"] */ .Z;
document.head.appendChild(style);

define(["@jupyter-widgets/base"], create);


/***/ }),

/***/ 5203:
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "Z": () => (/* export default binding */ __WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var gosling_js__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(7073);
/* harmony import */ var gosling_js__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(gosling_js__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _package_json__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(4147);



/** @param {typeof import("@jupyter-widgets/base")} base */
/* harmony default export */ function __WEBPACK_DEFAULT_EXPORT__(base) {

	class GoslingModel extends base.DOMWidgetModel {
		defaults() {
			return {
				...super.defaults(),

				_model_name: GoslingModel.model_name,
				_model_module: GoslingModel.model_module,
				_model_module_version: GoslingModel.model_module_version,

				_view_name: GoslingView.view_name,
				_view_module: GoslingView.view_module,
				_view_module_version: GoslingView.view_module_version,
			};
		}

		static model_name = 'GoslingModel';
		static model_module = _package_json__WEBPACK_IMPORTED_MODULE_1__/* .name */ .u2;
		static model_module_version = _package_json__WEBPACK_IMPORTED_MODULE_1__/* .version */ .i8;

		static view_name = 'GoslingView';
		static view_module = _package_json__WEBPACK_IMPORTED_MODULE_1__/* .name */ .u2;
		static view_module_version = _package_json__WEBPACK_IMPORTED_MODULE_1__/* .version */ .i8;
	}

	class GoslingView extends base.DOMWidgetView {

		async render() {
			let viewconf = JSON.parse(this.model.get("_viewconf"));
			let api = await gosling_js__WEBPACK_IMPORTED_MODULE_0__.embed(this.el, viewconf, {});
			console.log(api);

			this.model.on('msg:custom', msg => {
				msg = JSON.parse(msg);
				console.log(msg);
				try {
					let [fn, ...args] = msg;
					api[fn](...args);
				} catch (e) {
					console.error(e);
				}
			});
		}

	}

	return { GoslingModel, GoslingView };
}


/***/ }),

/***/ 1912:
/***/ ((module) => {

module.exports = "data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHN0eWxlPSJiYWNrZ3JvdW5kLWNvbG9yOiNmZmZmZmYwMCIgd2lkdGg9IjYiIGhlaWdodD0iNiI+PHBhdGggZD0iTTYgNkgwVjQuMmg0LjJWMEg2djZ6IiBvcGFjaXR5PSIuMzAyIi8+PC9zdmc+";

/***/ }),

/***/ 4147:
/***/ ((module) => {

module.exports = JSON.parse('{"u2":"gosling-widget","i8":"0.0.0"}');

/***/ })

}]);