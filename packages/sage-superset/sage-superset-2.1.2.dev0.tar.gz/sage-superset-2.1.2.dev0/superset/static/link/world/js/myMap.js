(function() {
    // 1. 实例化对象
    var myChart = echarts.init(document.querySelector(".map .chart"));
    // 2. 指定配置和数据
    // 2. 指定配置和数据
    var geoCoordMap = {
        杭州: [119.5313, 29.8773],
        Afghanistan: [33.93911, 67.709953],
        Albania: [41.153332, 20.168331],
        Argentina: [-38.416097, -63.616672],
        Armenia: [40.069099, 45.038189],
        Australia: [-25.274398, 133.775136],
        Belarus: [53.709807, 27.953389],
        Benin: [9.30769, 2.315834],
        Brazil: [-14.235004, -51.92528],
        Canada: [56.130366, -106.346771],
        Chile: [-35.675147, -71.542969],
        China: [30.274084, 120.155067],
        India: [20.593684, 78.96288],
        Japan: [36.204824, 138.252924]

    };

    var XAData = [
        [{ name: "杭州" }, { name: "Afghanistan", value: 100 }],
        [{ name: "杭州" }, { name: "Albania", value: 100 }],
        [{ name: "杭州" }, { name: "Argentina", value: 100 }],
        [{ name: "杭州" }, { name: "Armenia", value: 100 }],
        [{ name: "杭州" }, { name: "Australia", value: 100 }]
    ];

    var XNData = [
        [{ name: "杭州", }, { name: "Belarus", value: 100 }],
        [{ name: "杭州" }, { name: "Benin", value: 100 }],
        [{ name: "杭州" }, { name: "Brazil", value: 100 }],
        [{ name: "杭州" }, { name: "Canada", value: 100 }],
        [{ name: "杭州" }, { name: "Chile", value: 100 }]
    ];

    var YCData = [
        [{ name: "杭州", value: 100 }, { name: "India", value: 100 }],
        [{ name: "杭州", value: 100 }, { name: "Japan", value: 100 }],
        [{ name: "杭州", value: 100 }, { name: "杭州", value: 100 }]
    ];

    var planePath =
        "path://M1705.06,1318.313v-89.254l-319.9-221.799l0.073-208.063c0.521-84.662-26.629-121.796-63.961-121.491c-37.332-0.305-64.482,36.829-63.961,121.491l0.073,208.063l-319.9,221.799v89.254l330.343-157.288l12.238,241.308l-134.449,92.931l0.531,42.034l175.125-42.917l175.125,42.917l0.531-42.034l-134.449-92.931l12.238-241.308L1705.06,1318.313z";
    //var planePath = 'arrow';
    var convertData = function(data) {
        var res = [];
        for (var i = 0; i < data.length; i++) {
            var dataItem = data[i];

            var fromCoord = geoCoordMap[dataItem[0].name];
            var toCoord = geoCoordMap[dataItem[1].name];
            if (fromCoord && toCoord) {
                res.push({
                    fromName: dataItem[0].name,
                    toName: dataItem[1].name,
                    coords: [fromCoord, toCoord],
                    value: dataItem[1].value
                });
            }
        }
        return res;
    };

    var color = ["#fff", "#fff", "#fff"]; //航线的颜色
    var series = [];
    [
        ["杭州", XAData],
        ["杭州", XNData],
        ["杭州", YCData]
    ].forEach(function(item, i) {
        series.push({
            name: item[0] + " Top3",
            type: "lines",
            zlevel: 1,
            effect: {
                show: true,
                period: 6,
                trailLength: 0.7,
                color: "red", //arrow箭头的颜色
                symbolSize: 3
            },
            lineStyle: {
                normal: {
                    color: color[i],
                    width: 0,
                    curveness: 0.2
                }
            },
            data: convertData(item[1])
        }, {
            name: item[0] + " Top3",
            type: "lines",
            zlevel: 2,
            symbol: ["none", "arrow"],
            symbolSize: 10,
            effect: {
                show: true,
                period: 6,
                trailLength: 0,
                symbol: planePath,
                symbolSize: 15
            },
            lineStyle: {
                normal: {
                    color: color[i],
                    width: 1,
                    opacity: 0.6,
                    curveness: 0.2
                }
            },
            data: convertData(item[1])
        }, {
            name: item[0] + " Top3",
            type: "effectScatter",
            coordinateSystem: "geo",
            zlevel: 2,
            rippleEffect: {
                brushType: "stroke"
            },
            label: {
                normal: {
                    show: true,
                    position: "right",
                    formatter: "{b}"
                }
            },
            symbolSize: function(val) {
                return val[2] / 8;
            },
            itemStyle: {
                normal: {
                    color: color[i]
                },
                emphasis: {
                    areaColor: "#2B91B7"
                }
            },
            data: item[1].map(function(dataItem) {
                return {
                    name: dataItem[1].name,
                    value: geoCoordMap[dataItem[1].name].concat([dataItem[1].value])
                };
            })
        });
    });
    var option = {
        tooltip: {
            trigger: "item",
            formatter: function(params, ticket, callback) {
                if (params.seriesType == "effectScatter") {
                    return "线路：" + params.data.name + "" + params.data.value[2];
                } else if (params.seriesType == "lines") {
                    return (
                        params.data.fromName +
                        ">" +
                        params.data.toName +
                        "<br />" +
                        params.data.value
                    );
                } else {
                    return params.name;
                }
            }
        },

        geo: {
            map: "world",
            label: {
                emphasis: {
                    show: true,
                    color: "#fff"
                }
            },
            roam: false,
            //   放大我们的地图
            zoom: 1,
            itemStyle: {
                normal: {
                    areaColor: "rgba(43, 196, 243, 0.42)",
                    borderColor: "rgba(43, 196, 243, 1)",
                    borderWidth: 1
                },
                emphasis: {
                    areaColor: "#2B91B7"
                }
            }
        },
        series: series
    };
    myChart.setOption(option);
    window.addEventListener("resize", function() {
        myChart.resize();
    });
})();