define(['jquery', 'jquery.flot', 'jquery.flot.time'], function($) {
    var GRAPH_DATA = window.GRAPH_DATA;

    GRAPH_DATA.registrationGraph.options = {
        "series": {
            "lines": {"show": true, "lineWidth": 1},
            "points": {"show": true},
            "label": "Number of Registered Users Over Time"
        },
        "xaxis": {
            "mode": "time"
            /*,"timeformat": "%m/%d/%Y"*/
        },
        "yaxis": {
            "label": "Number of Users",
            "position": "left",
            "tickDecimals": 0
        },
    };
    GRAPH_DATA.userExperienceGraph.options = {
        "series": {
            "bars": {
                "show": true,
                "barWidth": 0.6,
                "align": "center"
            },
            "label": "Histogram of Number of Viewable Collections Per User"
        },
        "xaxis": {
            "mode": "categories",
            "label": "Number of Collections",
            "tickLength": 0,
            "tickSize": 1,
            "tickDecimals": 0,
            "min": 0
        },
        "yaxis": {
            "mode": "categories",
            "label": "Number of Users",
            "tickLength": 0,
            "tickSize": 1,
            "tickDecimals": 0
        }
    };

    var module = {
        initModule: function(el) {
            $.each(GRAPH_DATA, function(k, v) {
                console.log(k, " => ", v);
                $.plot("#"+k, [v.data], v.options);
            });
        }
    };
    return module;
});
