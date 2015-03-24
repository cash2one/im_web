define("dist/app/im/game_add/index",["$","helper","../../../app/common/tip","../../../lib/cmp/widget","../../../lib/util/base","../../../lib/util/class","../../../lib/util/event","../../../lib/util/aspect","../../../lib/util/attribute","../../../lib/cmp/daparser","../../../lib/cmp/auto-render","../../../lib/util/dom/sticky","../../../app/widget/game_form","../../common/tip","../../../mod/validate"],function(a){var b=a("$"),c=(a("helper"),a("../../../app/common/tip").self,a("../../../app/widget/game_form")),d=b(".push-add-form form");c(d)}),define("dist/app/common/tip",["$","../../lib/cmp/widget","../../lib/util/base","../../lib/util/class","../../lib/util/event","../../lib/util/aspect","../../lib/util/attribute","../../lib/cmp/daparser","../../lib/cmp/auto-render","../../lib/util/dom/sticky"],function(a,b,c){var d,e=a("$"),f=a("../../lib/cmp/widget"),g=a("../../lib/util/dom/sticky"),h=f.extend({attrs:{timer:null,hideTimer:null,timeout:3e3,template:'<div class="tips-pop"><span></span><a class="close" href="#" data-action="close">×</a></div>',top:99},events:{"click [data-action=close]":function(){return this.hide(),!1}},setup:function(){h.superclass.setup.call(this),g.fix(this.element)},show:function(a,b,c){c=c||{};var f=c.position;return this.element.find("a.close")[c.hideClose===!0?"hide":"show"](),this.element.children("span:first").text(a),f?(this.element.css(f),f.left===d&&this.element.css("left",(e(window).width()-this.element.width())/2)):this.element.css({left:(e(window).width()-this.element.width())/2,top:this.get("top")}),this.element.removeClass().addClass("tips-pop "+(b||"")),this.element.show(),this},hide:function(){return this.element.hide(),this.timer&&(clearTimeout(this.timer),this.timer=null),this},success:function(a){return this.show(a)},error:function(a){return this.show(a,"tips-failure")},auto:function(a,b,c){var d=this;return c=c||{},c.delay=0,c.hideClose=c.hideClose!==!1,this.delay(a,b,c),this.hideTimer&&(clearTimeout(this.hideTimer),this.hideTimer=null),this.hideTimer=setTimeout(function(){d.hideTimer=null,d.hide()},c.time||3e3),this},delay:function(a,b,c){var e=this,f="";return c=c||{},c.cls?f=c.cls:"error"===b&&(f="tips-failure"),this.timer&&clearTimeout(this.timer),this.timer=setTimeout(function(){e.timer=null,e.show(a,f,c)},c.delay===d?1e3:c.delay),this}});c.exports={common:(new h).render(),self:(new h).render()}}),define("dist/lib/cmp/widget",["../util/base","../util/class","../util/event","../util/aspect","../util/attribute","$","./daparser","./auto-render"],function(a,b,c){function d(){return"widget-"+w++}function e(a){return"[object String]"===v.call(a)}function f(a){return"[object Function]"===v.call(a)}function g(a){return x(document.documentElement,a)}function h(a){return a.charAt(0).toUpperCase()+a.substring(1)}function i(a){return f(a.events)&&(a.events=a.events()),a.events}function j(a,b){var c=a.match(y),d=c[1]+q+b.cid,e=c[2]||void 0;return e&&e.indexOf("{{")>-1&&(e=k(e,b)),{type:d,selector:e}}function k(a,b){return a.replace(z,function(a,c){for(var d,f=c.split("."),g=b;d=f.shift();)g=g===b.attrs?b.get(d):g[d];return e(g)?g:A})}function l(a){return null==a||void 0===a}var m=a("../util/base"),n=a("$"),o=a("./daparser"),p=a("./auto-render"),q=".delegate-events-",r="_onRender",s="data-widget-cid",t={},u=m.extend({propsInAttrs:["initElement","element","events"],element:null,events:null,attrs:{id:null,className:null,style:null,template:"<div></div>",model:null,parentNode:document.body},initialize:function(a){this.cid=d();var b=this._parseDataAttrsConfig(a);u.superclass.initialize.call(this,a?n.extend(b,a):b),this.parseElement(),this.initProps(),this.delegateEvents(),this.setup(),this._stamp(),this._isTemplate=!(a&&a.element)},_parseDataAttrsConfig:function(a){var b,c;return a&&(b=n(a.initElement?a.initElement:a.element)),b&&b[0]&&!p.isDataApiOff(b)&&(c=o.parseElement(b)),c},parseElement:function(){var a=this.element;if(a?this.element=n(a):this.get("template")&&this.parseElementFromTemplate(),!this.element||!this.element[0])throw new Error("element is invalid")},parseElementFromTemplate:function(){this.element=n(this.get("template"))},initProps:function(){},delegateEvents:function(a,b,c){if(0===arguments.length?(b=i(this),a=this.element):1===arguments.length?(b=a,a=this.element):2===arguments.length?(c=b,b=a,a=this.element):(a||(a=this.element),this._delegateElements||(this._delegateElements=[]),this._delegateElements.push(n(a))),e(b)&&f(c)){var d={};d[b]=c,b=d}for(var g in b)if(b.hasOwnProperty(g)){var h=j(g,this),k=h.type,l=h.selector;!function(b,c){var d=function(a){return f(b)?b.call(c,a):c[b](a)};l?n(a).on(k,l,d):n(a).on(k,d)}(b[g],this)}return this},undelegateEvents:function(a,b){if(b||(b=a,a=null),0===arguments.length){var c=q+this.cid;if(this.element&&this.element.off(c),this._delegateElements)for(var d in this._delegateElements)this._delegateElements.hasOwnProperty(d)&&this._delegateElements[d].off(c)}else{var e=j(b,this);a?n(a).off(e.type,e.selector):this.element&&this.element.off(e.type,e.selector)}return this},setup:function(){},render:function(){this.rendered||(this._renderAndBindAttrs(),this.rendered=!0);var a=this.get("parentNode");if(a&&!g(this.element[0])){var b=this.constructor.outerBoxClass;if(b){var c=this._outerBox=n("<div></div>").addClass(b);c.append(this.element).appendTo(a)}else this.element.appendTo(a)}return this},_renderAndBindAttrs:function(){var a=this,b=a.attrs;for(var c in b)if(b.hasOwnProperty(c)){var d=r+h(c);if(this[d]){var e=this.get(c);l(e)||this[d](e,void 0,c),function(b){a.on("change:"+c,function(c,d,e){a[b](c,d,e)})}(d)}}},_onRenderId:function(a){this.element.attr("id",a)},_onRenderClassName:function(a){this.element.addClass(a)},_onRenderStyle:function(a){this.element.css(a)},_stamp:function(){var a=this.cid;(this.initElement||this.element).attr(s,a),t[a]=this},$:function(a){return this.element.find(a)},destroy:function(){this.undelegateEvents(),delete t[this.cid],this.element&&this._isTemplate&&(this.element.off(),this._outerBox?this._outerBox.remove():this.element.remove()),this.element=null,u.superclass.destroy.call(this)}});n(window).unload(function(){for(var a in t)t[a].destroy()}),u.query=function(a){var b,c=n(a).eq(0);return c&&(b=c.attr(s)),t[b]},u.autoRender=p.autoRender,u.autoRenderAll=p.autoRenderAll,u.StaticsWhiteList=["autoRender"],c.exports=u;var v=Object.prototype.toString,w=0,x=n.contains||function(a,b){return!!(16&a.compareDocumentPosition(b))},y=/^(\S+)\s*(.*)$/,z=/{{([^}]+)}}/g,A="INVALID_SELECTOR"}),define("dist/lib/util/base",["./class","./event","./aspect","./attribute"],function(a,b,c){function d(a,b){for(var c in b)if(b.hasOwnProperty(c)){var d="_onChange"+e(c);a[d]&&a.on("change:"+c,a[d])}}function e(a){return a.charAt(0).toUpperCase()+a.substring(1)}var f=a("./class"),g=a("./event"),h=a("./aspect"),i=a("./attribute"),j=f.create({Implements:[g,h,i],initialize:function(a){this.initAttrs(a),d(this,this.attrs)},destroy:function(){this.off();for(var a in this)this.hasOwnProperty(a)&&delete this[a];this.destroy=function(){}}});c.exports=j}),define("dist/lib/util/class",[],function(a,b,c){function d(a){return this instanceof d||!l(a)?void 0:g(a)}function e(){}function f(a){var b,c;for(b in a)c=a[b],d.Mutators.hasOwnProperty(b)?d.Mutators[b].call(this,c):this.prototype[b]=c}function g(a){return a.extend=d.extend,a.implement=f,a}function h(a,b,c){for(var d in b)if(b.hasOwnProperty(d)){if(c&&-1===m(c,d))continue;"prototype"!==d&&(a[d]=b[d])}}c.exports=d,d.extend=function(a){return a||(a={}),a.Extends=this,d.create(a)},d.create=function(a,b){function c(){a.apply(this,arguments),this.constructor===c&&this.initialize&&this.initialize.apply(this,arguments)}return l(a)||(b=a,a=null),b||(b={}),a||(a=b.Extends||d),b.Extends=a,a!==d&&h(c,a,a.StaticsWhiteList),f.call(c,b),g(c)};var i=Object.__proto__?function(a){return{__proto__:a}}:function(a){return e.prototype=a,new e};d.Mutators={Extends:function(a){var b=this.prototype,c=i(a.prototype);h(c,b),c.constructor=this,this.prototype=c,this.superclass=a.prototype},Implements:function(a){k(a)||(a=[a]);for(var b,c=this.prototype;b=a.shift();)h(c,b.prototype||b)},Statics:function(a){h(this,a)}};var j=Object.prototype.toString,k=Array.isArray||function(a){return"[object Array]"===j.call(a)},l=function(a){return"[object Function]"===j.call(a)},m=Array.prototype.indexOf?function(a,b){return a.indexOf(b)}:function(a,b){for(var c=0,d=a.length;d>c;c++)if(a[c]===b)return c;return-1}}),define("dist/lib/util/event",[],function(a,b,c){function d(){}function e(a,b,c,d){var e;if(a)for(var f=0,g=a.length;g>f;f+=2)e=a[f].apply(a[f+1]||c,b),e===!1&&d.status&&(d.status=!1)}var f=/\s+/;c.exports=d,d.prototype.on=function(a,b,c){var d,e,g;if(!b)return this;for(d=this.__events||(this.__events={}),a=a.split(f);e=a.shift();)g=d[e]||(d[e]=[]),g.push(b,c);return this},d.prototype.off=function(a,b,c){var d,e,h,i;if(!(d=this.__events))return this;if(!(a||b||c))return delete this.__events,this;for(a=a?a.split(f):g(d);e=a.shift();)if(h=d[e])if(b||c)for(i=h.length-2;i>=0;i-=2)b&&h[i]!==b||c&&h[i+1]!==c||h.splice(i,2);else delete d[e];return this},d.prototype.trigger=function(a){var b,c,d,g,h,i,j=[],k={status:!0};if(!(b=this.__events))return this;for(a=a.split(f),h=1,i=arguments.length;i>h;h++)j[h-1]=arguments[h];for(;c=a.shift();)(d=b.all)&&(d=d.slice()),(g=b[c])&&(g=g.slice()),e(g,j,this,k),e(d,[c].concat(j),this,k);return k.status},d.mixTo=function(a){a=a.prototype||a;var b=d.prototype;for(var c in b)b.hasOwnProperty(c)&&(a[c]=b[c])};var g=Object.keys;g||(g=function(a){var b=[];for(var c in a)a.hasOwnProperty(c)&&b.push(c);return b})}),define("dist/lib/util/aspect",[],function(a,b,c){function d(a,b,c,d){for(var g,i,j=b.split(h);g=j.shift();)i=e(this,g),i.__isAspected||f.call(this,g),this.on(a+":"+g,c,d);return this}function e(a,b){var c=a[b];if(!c)throw new Error("Invalid method name: "+b);return c}function f(a){var b=this[a];this[a]=function(){var c=Array.prototype.slice.call(arguments),d=["before:"+a].concat(c);if(this.trigger.apply(this,d)!==!1){var e=b.apply(this,arguments),f=["after:"+a,e].concat(c);return this.trigger.apply(this,f),e}},this[a].__isAspected=!0}var g={before:function(a,b,c){return d.call(this,"before",a,b,c)},after:function(a,b,c){return d.call(this,"after",a,b,c)}};c.exports=g;var h=/\s+/}),define("dist/lib/util/attribute",[],function(a,b,c){function d(a){return"[object String]"===u.call(a)}function e(a){return"[object Function]"===u.call(a)}function f(a){return null!==a&&a===a.window}function g(a){if(!a||"[object Object]"!==u.call(a)||a.nodeType||f(a))return!1;try{if(a.constructor&&!v.call(a,"constructor")&&!v.call(a.constructor.prototype,"isPrototypeOf"))return!1}catch(b){return!1}var c;if(t)for(c in a)return v.call(a,c);for(c in a);return void 0===c||v.call(a,c)}function h(a){if(!a||"[object Object]"!==u.call(a)||a.nodeType||f(a)||!a.hasOwnProperty)return!1;for(var b in a)if(a.hasOwnProperty(b))return!1;return!0}function i(a,b){var c,d;for(c in b)if(b.hasOwnProperty(c)){if(d=b[c],w(d))d=d.slice();else if(g(d)){var e=a[c];g(e)||(e={}),d=i(e,d)}a[c]=d}return a}function j(a,b,c){for(var d=[],e=b.constructor.prototype;e;)e.hasOwnProperty("attrs")||(e.attrs={}),l(c,e.attrs,e),h(e.attrs)||d.unshift(e.attrs),e=e.constructor.superclass;for(var f=0,g=d.length;g>f;f++)i(a,p(d[f]))}function k(a,b){i(a,p(b,!0))}function l(a,b,c,d){for(var e=0,f=a.length;f>e;e++){var g=a[e];c.hasOwnProperty(g)&&(b[g]=d?b.get(g):c[g])}}function m(a,b){for(var c in b)if(b.hasOwnProperty(c)){var d,f=b[c].value;e(f)&&(d=c.match(y))&&(a[d[1]](n(d[2]),f),delete b[c])}}function n(a){var b=a.match(z),c=b[1]?"change:":"";return c+=b[2].toLowerCase()+b[3]}function o(a,b,c){var d={silent:!0};a.__initializingAttrs=!0;for(var e in c)c.hasOwnProperty(e)&&b[e].setter&&a.set(e,c[e],d);delete a.__initializingAttrs}function p(a,b){var c={};for(var d in a){var e=a[d];c[d]=!b&&g(e)&&q(e,A)?e:{value:e}}return c}function q(a,b){for(var c=0,d=b.length;d>c;c++)if(a.hasOwnProperty(b[c]))return!0;return!1}function r(a){return null===a||(d(a)||w(a))&&0===a.length||h(a)}function s(a,b){if(a===b)return!0;if(r(a)&&r(b))return!0;var c=u.call(a);if(c!==u.call(b))return!1;switch(c){case"[object String]":return a===String(b);case"[object Number]":return a!==+a?b!==+b:0===a?1/a===1/b:a===+b;case"[object Date]":case"[object Boolean]":return+a===+b;case"[object RegExp]":return a.source===b.source&&a.global===b.global&&a.multiline===b.multiline&&a.ignoreCase===b.ignoreCase;case"[object Array]":var d=a.toString(),e=b.toString();return-1===d.indexOf("[object")&&-1===e.indexOf("[object")&&d===e}if("object"!=typeof a||"object"!=typeof b)return!1;if(g(a)&&g(b)){if(!s(x(a),x(b)))return!1;for(var f in a)if(a[f]!==b[f])return!1;return!0}return!1}var t,u=Object.prototype.toString,v=Object.prototype.hasOwnProperty;!function(){function a(){this.x=1}var b=[];a.prototype={valueOf:1,y:1};for(var c in new a)b.push(c);t="x"!==b[0]}();var w=Array.isArray||function(a){return"[object Array]"===u.call(a)},x=Object.keys;x||(x=function(a){var b=[];for(var c in a)a.hasOwnProperty(c)&&b.push(c);return b});var y=/^(on|before|after)([A-Z].*)$/,z=/^(Change)?([A-Z])(.*)/,A=["value","getter","setter","readOnly"],B={initAttrs:function(a){var b=this.attrs={},c=this.propsInAttrs||[];j(b,this,c),a&&k(b,a),o(this,b,a),m(this,b),l(c,this,b,!0)},get:function(a){var b=this.attrs[a]||{},c=b.value;return b.getter?b.getter.call(this,c,a):c},set:function(a,b,c){var e={};d(a)?e[a]=b:(e=a,c=b),c||(c={});var f=c.silent,h=c.override,j=this.attrs,k=this.__changedAttrs||(this.__changedAttrs={});for(a in e)if(e.hasOwnProperty(a)){var l=j[a]||(j[a]={});if(b=e[a],l.readOnly)throw new Error("This attribute is readOnly: "+a);l.setter&&(b=l.setter.call(this,b,a));var m=this.get(a);!h&&g(m)&&g(b)&&(b=i(i({},m),b)),j[a].value=b,this.__initializingAttrs||s(m,b)||(f?k[a]=[b,m]:this.trigger("change:"+a,b,m,a))}return this},change:function(){var a=this.__changedAttrs;if(a){for(var b in a)if(a.hasOwnProperty(b)){var c=a[b];this.trigger("change:"+b,c[0],c[1],b)}delete this.__changedAttrs}return this},_isPlainObject:g};c.exports=B}),define("dist/lib/cmp/daparser",["$"],function(a,b){function c(a){return a.toLowerCase().replace(g,function(a,b){return(b+"").toUpperCase()})}function d(a){for(var b in a)if(a.hasOwnProperty(b)){var c=a[b];if("string"!=typeof c)continue;h.test(c)?(c=c.replace(/'/g,'"'),a[b]=d(i(c))):a[b]=e(c)}return a}function e(a){if("false"===a.toLowerCase())a=!1;else if("true"===a.toLowerCase())a=!0;else if(/\d/.test(a)&&/[^a-z]/i.test(a)){var b=parseFloat(a);b+""===a&&(a=b)}return a}var f=a("$");b.parseElement=function(a,b){a=f(a)[0];var e={};if(a.dataset)e=f.extend({},a.dataset);else for(var g=a.attributes,h=0,i=g.length;i>h;h++){var j=g[h],k=j.name;0===k.indexOf("data-")&&(k=c(k.substring(5)),e[k]=j.value)}return b===!0?e:d(e)};var g=/-([a-z])/g,h=/^\s*[\[{].*[\]}]\s*$/,i=this.JSON?JSON.parse:f.parseJSON}),define("dist/lib/cmp/auto-render",["$"],function(a,b){var c=a("$"),d="data-widget-auto-rendered";b.autoRender=function(a){return new this(a).render()},b.autoRenderAll=function(a,e){"function"==typeof a&&(e=a,a=null),a=c(a||document.body);var f=[],g=[];a.find("[data-widget]").each(function(a,c){b.isDataApiOff(c)||(f.push(c.getAttribute("data-widget").toLowerCase()),g.push(c))}),f.length&&seajs.use(f,function(){for(var a=0;a<arguments.length;a++){var b=arguments[a],f=c(g[a]);if(!f.attr(d)){var h={initElement:f,renderType:"auto"},i=f.attr("data-widget-role");h[i?i:"element"]=f,b.autoRender&&b.autoRender(h),f.attr(d,"true")}}e&&e()})};var e="off"===c(document.body).attr("data-api");b.isDataApiOff=function(a){var b=c(a).attr("data-api");return"off"===b||"on"!==b&&e}}),define("dist/lib/util/dom/sticky",["$"],function(a,b,c){function d(a,b,c){return new g({element:a,marginTop:b||0,callback:c}).render()}function e(){return!n}function f(){if(m)return!1;var a=i[0].body;if(i[0].createElement&&a&&a.appendChild&&a.removeChild){var b,c=i[0].createElement("div"),d=function(a){return window.getComputedStyle?window.getComputedStyle(c).getPropertyValue(a):c.currentStyle.getAttribute(a)};a.appendChild(c);for(var e=0;e<j.length&&(c.style.cssText="position:"+j[e]+"sticky;visibility:hidden;",!(b=-1!==d("position").indexOf("sticky")));e++);return c.parentNode.removeChild(c),b}}function g(a){this.options=a||{},this.elem=h(this.options.element),this.callback=a.callback||function(){},this.marginTop=a.marginTop||0,this._stickyId=k++}var h=a("$"),i=h(document),j=["-webkit-","-ms-","-o-","-moz-",""],k=0,l=(window.navigator.userAgent||"").toLowerCase(),m=-1!==l.indexOf("msie"),n=-1!==l.indexOf("msie 6"),o=f(),p=e();d.stick=d,d.fix=function(a){return new g({element:a,marginTop:Number.MAX_VALUE}).render()},d.isPositionStickySupported=o,d.isPositionFixedSupported=p,g.prototype.render=function(){var a,b=this;if(this.elem.length&&!this.elem.data("bind-sticked")){this._originTop=this.elem.offset().top,this.marginTop===Number.MAX_VALUE&&(a=!0,this.marginTop=this._originTop),this._originStyles={position:null,top:null,left:null};for(var c in this._originStyles)this._originStyles.hasOwnProperty(c)&&(this._originStyles[c]=this.elem.css(c));var e;if(d.isPositionStickySupported&&!a){e=this._supportSticky;for(var f="",g=0;g<j.length;g++)f+="position:"+j[g]+"sticky;";this.elem[0].style.cssText+=f+"top: "+this.marginTop+"px;"}else d.isPositionFixedSupported?e=this._supportFixed:(e=this._supportAbsolute,h('<style type="text/css"> * html{ background:url(null) no-repeat fixed; } </style>').appendTo("head"));return e.call(this),h(window).on("scroll."+this._stickyId,function(){b.elem.is(":visible")&&e.call(b)}),this.elem.data("bind-sticked",!0),this}},g.prototype._supportFixed=function(){var a=this._originTop-i.scrollTop();!this.elem.data("sticked")&&a<=this.marginTop?(this._addPlaceholder(),this.elem.css({position:"fixed",top:this.marginTop,left:this.elem.offset().left}),this.elem.data("sticked",!0),this.callback.call(this,!0)):this.elem.data("sticked")&&a>this.marginTop&&this._restore()},g.prototype._supportAbsolute=function(){var a=this._originTop-i.scrollTop();a<=this.marginTop?(this.elem.data("sticked")||(this._addPlaceholder(),this.elem.data("sticked",!0),this.callback.call(this,!0)),this.elem.css({position:"absolute",top:this.marginTop+i.scrollTop()})):this.elem.data("sticked")&&a>this.marginTop&&this._restore()},g.prototype._supportSticky=function(){var a=this._originTop-i.scrollTop();!this.elem.data("sticked")&&a<=this.marginTop?(this.elem.data("sticked",!0),this.callback.call(this,!0)):this.elem.data("sticked")&&a>this.marginTop&&this.callback.call(this,!1)},g.prototype._restore=function(){this._removePlaceholder(),this.elem.css(this._originStyles),this.elem.data("sticked",!1),this.callback.call(this,!1)},g.prototype._addPlaceholder=function(){var a=!1,b=this.elem.css("position");("static"===b||"relative"===b)&&(a=!0),"block"!==this.elem.css("display")&&(a=!1),a&&(this._placeholder=h('<div style="visibility:hidden;margin:0;padding:0;"></div>'),this._placeholder.width(this.elem.outerWidth(!0)).height(this.elem.outerHeight(!0)).css("float",this.elem.css("float")).insertAfter(this.elem))},g.prototype._removePlaceholder=function(){this._placeholder&&this._placeholder.remove()},g.prototype.destroy=function(){this._restore(),this.elem.data("bind-sticked",!1),h(window).off("scroll."+this._stickyId)},c.exports=d}),define("dist/app/widget/game_form",["../common/tip","$","../../lib/cmp/widget","../../lib/util/base","../../lib/util/class","../../lib/util/event","../../lib/util/aspect","../../lib/util/attribute","../../lib/cmp/daparser","../../lib/cmp/auto-render","../../lib/util/dom/sticky","helper","../../mod/validate"],function(a,b,c){function d(a){a.find(".android-extra, .ios-extra");$.each(["ios","android"],function(b,c){var d=a.find("."+c+"-extra"),e=$(".platform-item."+c);e.click(function(){if(e.hasClass("checked")&&e.hasClass("is-select"))return!1;var a=e.hasClass("checked");e[a?"removeClass":"addClass"]("checked"),d[a?"hide":"show"]()})})}function e(a){a.on("submit",function(){if(0===a.find(".checked").length)return Tip.auto("至少要勾选一个平台","error"),!1;var b=a.find(".android"),c=a.find(".client-android-identity"),d=a.find(".ios"),e=a.find(".client-ios-identity"),f=$.trim(c.val());if(b.hasClass("checked")){if(0===f.length)return Tip.auto("请填写包名","error"),c.addClass("ipt-error"),!1;c.removeClass("ipt-error")}if(f=$.trim(e.val()),d.hasClass("checked")){if(0===f.length)return Tip.auto("请填写BundleID","error"),e.addClass("ipt-error"),!1;e.removeClass("ipt-error")}var g=a.find("#develop_apns");if(g.val()&&"p12"!=g.val().split(".").pop())return Tip.auto("请上传 `.p12` 格式的文件","error"),g.addClass("ipt-error"),!1;var h=a.find("#production_apns");return h.val()&&"p12"!=h.val().split(".").pop()?(Tip.auto("请上传 `.p12` 格式的文件","error"),h.addClass("ipt-error"),!1):!0})}Tip=a("../common/tip").self,$=a("$"),helper=a("helper"),Validate=a("../../mod/validate"),c.exports=function(a,b){d(a),e(a,b)}}),define("dist/mod/validate",["$"],function(a,b,c){function d(a,b){if(this.options=e.extend({},h,b),!a)throw new Error("A form object is requried");a.on("submit",e.proxy(function(b){this.validate(a)||(b.preventDefault(),b.stopPropagation(),b.stopImmediatePropagation())},this)),this.fieldsToValidate=a.find("[data-validate]"),this.form=a,this.bindInvalid()}var e=a("$"),f={"[data-required]":{rule:function(a){return!!e.trim(a.val()).length},invalid:"请填写{{name}}。"}},g={all:function(a,b,c){var d=!0;return e.each(a,function(e,f){d=d&&b.call(c,e,f,a)}),d}},h={invalidSelector:".error"};d.prototype={constructor:d.prototype.constructor,validate:function(){this.clearInvalids();var a=!0;return this.fieldsToValidate.each(e.proxy(function(b,c){c=e(c),this.validateElem(c)||(a=!1)},this)),a},validateElem:function(a){return g.all(f,function(b,c){if(!a.is(b))return!0;var d=c.rule(a);if(d)return!0;var e=c.invalid;return a.trigger("invalid",e&&e.replace("{{name}}",a.data("name")||"文字")),d},this)},bindInvalid:function(){this.form.on("invalid",e.proxy(this.handleInvalid,this))},handleInvalid:function(a,b){var c=e(a.target),d=c.closest("td").find(this.options.invalidSelector);d.text(b),c.addClass("ipt-error")},clearInvalids:function(){this.form.find(this.options.invalidSelector).html("&nbsp;"),this.fieldsToValidate.removeClass("ipt-error")}},c.exports=d});