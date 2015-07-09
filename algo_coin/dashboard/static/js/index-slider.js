jQuery.easing.jswing = jQuery.easing.swing;
jQuery.extend(jQuery.easing, {
    def: "easeOutQuad",
    swing: function (e, f, a, h, g) {
        return jQuery.easing[jQuery.easing.def](e, f, a, h, g)
    },
    easeInQuad: function (e, f, a, h, g) {
        return h * (f /= g) * f + a
    },
    easeOutQuad: function (e, f, a, h, g) {
        return -h * (f /= g) * (f - 2) + a
    },
    easeInOutQuad: function (e, f, a, h, g) {
        if ((f /= g / 2) < 1) {
            return h / 2 * f * f + a
        }
        return -h / 2 * ((--f) * (f - 2) - 1) + a
    },
    easeInCubic: function (e, f, a, h, g) {
        return h * (f /= g) * f * f + a
    },
    easeOutCubic: function (e, f, a, h, g) {
        return h * ((f = f / g - 1) * f * f + 1) + a
    },
    easeInOutCubic: function (e, f, a, h, g) {
        if ((f /= g / 2) < 1) {
            return h / 2 * f * f * f + a
        }
        return h / 2 * ((f -= 2) * f * f + 2) + a
    },
    easeInQuart: function (e, f, a, h, g) {
        return h * (f /= g) * f * f * f + a
    },
    easeOutQuart: function (e, f, a, h, g) {
        return -h * ((f = f / g - 1) * f * f * f - 1) + a
    },
    easeInOutQuart: function (e, f, a, h, g) {
        if ((f /= g / 2) < 1) {
            return h / 2 * f * f * f * f + a
        }
        return -h / 2 * ((f -= 2) * f * f * f - 2) + a
    },
    easeInQuint: function (e, f, a, h, g) {
        return h * (f /= g) * f * f * f * f + a
    },
    easeOutQuint: function (e, f, a, h, g) {
        return h * ((f = f / g - 1) * f * f * f * f + 1) + a
    },
    easeInOutQuint: function (e, f, a, h, g) {
        if ((f /= g / 2) < 1) {
            return h / 2 * f * f * f * f * f + a
        }
        return h / 2 * ((f -= 2) * f * f * f * f + 2) + a
    },
    easeInSine: function (e, f, a, h, g) {
        return -h * Math.cos(f / g * (Math.PI / 2)) + h + a
    },
    easeOutSine: function (e, f, a, h, g) {
        return h * Math.sin(f / g * (Math.PI / 2)) + a
    },
    easeInOutSine: function (e, f, a, h, g) {
        return -h / 2 * (Math.cos(Math.PI * f / g) - 1) + a
    },
    easeInExpo: function (e, f, a, h, g) {
        return (f == 0) ? a : h * Math.pow(2, 10 * (f / g - 1)) + a
    },
    easeOutExpo: function (e, f, a, h, g) {
        return (f == g) ? a + h : h * (-Math.pow(2, -10 * f / g) + 1) + a
    },
    easeInOutExpo: function (e, f, a, h, g) {
        if (f == 0) {
            return a
        }
        if (f == g) {
            return a + h
        }
        if ((f /= g / 2) < 1) {
            return h / 2 * Math.pow(2, 10 * (f - 1)) + a
        }
        return h / 2 * (-Math.pow(2, -10 * --f) + 2) + a
    },
    easeInCirc: function (e, f, a, h, g) {
        return -h * (Math.sqrt(1 - (f /= g) * f) - 1) + a
    },
    easeOutCirc: function (e, f, a, h, g) {
        return h * Math.sqrt(1 - (f = f / g - 1) * f) + a
    },
    easeInOutCirc: function (e, f, a, h, g) {
        if ((f /= g / 2) < 1) {
            return -h / 2 * (Math.sqrt(1 - f * f) - 1) + a
        }
        return h / 2 * (Math.sqrt(1 - (f -= 2) * f) + 1) + a
    },
    easeInElastic: function (f, h, e, l, k) {
        var i = 1.70158;
        var j = 0;
        var g = l;
        if (h == 0) {
            return e
        }
        if ((h /= k) == 1) {
            return e + l
        }
        if (!j) {
            j = k * 0.3
        }
        if (g < Math.abs(l)) {
            g = l;
            var i = j / 4
        } else {
            var i = j / (2 * Math.PI) * Math.asin(l / g)
        }
        return -(g * Math.pow(2, 10 * (h -= 1)) * Math.sin((h * k - i) * (2 * Math.PI) / j)) + e
    },
    easeOutElastic: function (f, h, e, l, k) {
        var i = 1.70158;
        var j = 0;
        var g = l;
        if (h == 0) {
            return e
        }
        if ((h /= k) == 1) {
            return e + l
        }
        if (!j) {
            j = k * 0.3
        }
        if (g < Math.abs(l)) {
            g = l;
            var i = j / 4
        } else {
            var i = j / (2 * Math.PI) * Math.asin(l / g)
        }
        return g * Math.pow(2, -10 * h) * Math.sin((h * k - i) * (2 * Math.PI) / j) + l + e
    },
    easeInOutElastic: function (f, h, e, l, k) {
        var i = 1.70158;
        var j = 0;
        var g = l;
        if (h == 0) {
            return e
        }
        if ((h /= k / 2) == 2) {
            return e + l
        }
        if (!j) {
            j = k * (0.3 * 1.5)
        }
        if (g < Math.abs(l)) {
            g = l;
            var i = j / 4
        } else {
            var i = j / (2 * Math.PI) * Math.asin(l / g)
        }
        if (h < 1) {
            return -0.5 * (g * Math.pow(2, 10 * (h -= 1)) * Math.sin((h * k - i) * (2 * Math.PI) / j)) + e
        }
        return g * Math.pow(2, -10 * (h -= 1)) * Math.sin((h * k - i) * (2 * Math.PI) / j) * 0.5 + l + e
    },
    easeInBack: function (e, f, a, i, h, g) {
        if (g == undefined) {
            g = 1.70158
        }
        return i * (f /= h) * f * ((g + 1) * f - g) + a
    },
    easeOutBack: function (e, f, a, i, h, g) {
        if (g == undefined) {
            g = 0.70158
        }
        return i * ((f = f / h - 1) * f * ((g + 1) * f + g) + 1) + a
    },
    easeInOutBack: function (e, f, a, i, h, g) {
        if (g == undefined) {
            g = 1.70158
        }
        if ((f /= h / 2) < 1) {
            return i / 2 * (f * f * (((g *= (1.525)) + 1) * f - g)) + a
        }
        return i / 2 * ((f -= 2) * f * (((g *= (1.525)) + 1) * f + g) + 2) + a
    },
    easeInBounce: function (e, f, a, h, g) {
        return h - jQuery.easing.easeOutBounce(e, g - f, 0, h, g) + a
    },
    easeOutBounce: function (e, f, a, h, g) {
        if ((f /= g) < (1 / 2.75)) {
            return h * (7.5625 * f * f) + a
        } else {
            if (f < (2 / 2.75)) {
                return h * (7.5625 * (f -= (1.5 / 2.75)) * f + 0.75) + a
            } else {
                if (f < (2.5 / 2.75)) {
                    return h * (7.5625 * (f -= (2.25 / 2.75)) * f + 0.9375) + a
                } else {
                    return h * (7.5625 * (f -= (2.625 / 2.75)) * f + 0.984375) + a
                }
            }
        }
    },
    easeInOutBounce: function (e, f, a, h, g) {
        if (f < g / 2) {
            return jQuery.easing.easeInBounce(e, f * 2, 0, h, g) * 0.5 + a
        }
        return jQuery.easing.easeOutBounce(e, f * 2 - g, 0, h, g) * 0.5 + h * 0.5 + a
    }
});

var center = $(window).width() / 2;
$(document).ready(function () {
    function d() {
        $(".slide.active img").each(function () {
            var g = parseInt($(this).attr("class").split(" ")[1].replace("left", ""));
            var i = g + center;
            var h = parseInt($(this).attr("class").split(" ")[3].replace("t", ""));
            var f = parseInt($(this).attr("class").split(" ")[4].replace("z", ""));
            if ($(this).hasClass("fade")) {
                $(this).css({
                    left: i,
                    top: h,
                    "z-index": f
                })
            } else {
                $(this).css({
                    left: i,
                    top: h,
                    "z-index": f
                }).show()
            }
        });
        setTimeout(function () {
            $(".slide.active img.fade,.slide.active .info").fadeIn(600, "easeInOutQuad", function () {
                $("#feature_slider").removeClass()
            })
        }, 800)
    }
    function c() {
        $("#feature_slider").addClass("disabled").append('<ul id="pagination" /><a href="" id="slide-left" /><a href="" id="slide-right" />');
        $("#feature_slider article").each(function () {
            $("#pagination").append('<li><a href="#' + $(this).attr("id") + '">' + $(this).index() + "</a></li>")
        });
        $("#pagination li:first").addClass("active");
        $("#pagination").css({
            left: ($(window).width() - $("#pagination li").length * 14) / 2
        });
        var h = 0;

        function j() {
            $(".slide.active img").each(function () {
                var l = parseInt($(this).attr("class").split(" ")[1].replace("left", ""));
                var q = l + center;
                // var p = parseInt($(this).attr("class").split(" ")[2].replace("st", ""));
                var p = 400;
                var n = parseInt($(this).attr("class").split(" ")[2].replace("sp", ""));
                var o = parseInt($(this).attr("class").split(" ")[3].replace("t", ""));
                var k = parseInt($(this).attr("class").split(" ")[4].replace("z", ""));
                if ($(this).hasClass("fade")) {
                    $(this).css({
                        left: q,
                        top: o,
                        "z-index": k
                    })
                } else {
                    if ($("#feature_slider").hasClass("scrollLeft")) {
                        var m = -$(this).width() - p
                    } else {
                        var m = $(window).width() + p
                    }
                    $(this).css({
                        left: m,
                        top: o,
                        "z-index": k
                    }).show();
                    $(this).animate({
                        left: q
                    }, n, "easeOutQuad")
                }
            });
            setTimeout(function () {
                $(".slide.active img.fade,.slide.active .info").fadeIn(600, "easeInOutQuad", function () {
                    $("#feature_slider").removeClass()
                })
            }, 600)
        }
        function g() {
            $(".slide.active").removeClass("active").addClass("previous");
            $(".slide.previous img").not(".fade").each(function () {
                // var l = parseInt($(this).attr("class").split(" ")[2].replace("st", ""));
                var l = 400;
                var k = parseInt($(this).attr("class").split(" ")[2].replace("sp", ""));
                if ($("#feature_slider").hasClass("scrollLeft")) {
                    $(this).animate({
                        left: $(window).width() + l
                    }, k, "easeInQuad")
                } else {
                    $(this).animate({
                        left: -$(this).width() - l
                    }, k, "easeInQuad")
                }
            });
            // speed of transitions
            $(".slide.previous img.fade,.slide.previous .info").fadeOut(600, "easeInQuad", function () {
                $(".slide.next").removeClass("next").addClass("active").fadeIn(500, "easeInOutQuad", function () {
                    $(".slide.previous").removeClass("previous").fadeOut(500, "easeInOutQuad");
                    j()
                })
            })
        }
        $(".slide:first").addClass("active").fadeIn(500, "easeInOutQuad", function () {
            $("#slide-left, #slide-right, #pagination").fadeIn(200, "easeInOutQuad", function () {
                j()
            })
        });
        $("#pagination li").not("active").click(function () {
            clearInterval(f);
            if ($(this).index() < $("#pagination li.active").index()) {
                $("#feature_slider").addClass("scrollLeft")
            }
            if (!$("#feature_slider").hasClass("disabled")) {
                $("#feature_slider").addClass("disabled");
                $("#pagination li.active").removeClass();
                $(this).addClass("active");
                $($(this).find("a").attr("href")).addClass("next");
                g()
            }
            return false
        });
        $("#slide-left").click(function () {
            clearInterval(f);
            if (!$("#feature_slider").hasClass("disabled")) {
                $("#feature_slider").addClass("disabled");
                if ($("#pagination li:first").hasClass("active")) {
                    $("#pagination li.active").removeClass();
                    $("#pagination li:last").addClass("active");
                    $("#feature_slider article:last").addClass("next")
                } else {
                    $("#pagination li.active").removeClass().prev().addClass("active");
                    $("#feature_slider article.active").prev().addClass("next")
                }
                $("#feature_slider").addClass("scrollLeft");
                g()
            }
            return false
        });

        function i() {
            if (!$("#feature_slider").hasClass("disabled")) {
                $("#feature_slider").addClass("disabled");
                if ($("#pagination li:last").hasClass("active")) {
                    $("#pagination li.active").removeClass();
                    $("#pagination li:first").addClass("active");
                    $("#feature_slider article:first").addClass("next")
                } else {
                    $("#pagination li.active").removeClass().next().addClass("active");
                    $("#feature_slider article.active").next().addClass("next")
                }
                g()
            }
        }
        $("#slide-right").click(function () {
            clearInterval(f);
            i();
            return false
        });
        var f = setInterval(function () {
            i()
        }, 5000)
    }
    c();
    $(window).resize(function () {
        $("#pagination").css({
            left: ($(window).width() - $("#pagination li").length * 14) / 2
        });
        center = $(window).width() / 2;
        d()
    });
});
