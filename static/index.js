// const {
//     log,
//     error
// } = console;

// const getData = async () => {
//     const resp = await fetch('http://127.0.0.1:5001/BTCUSDT/1m');
//     const data = await resp.json();
//     return data;
// };

// // getData();

// // createObj  genData setObj
// const renderChart = async () => {
//     const chartProperties = {
//         timeScale: {
//             timeVisible: true,
//             secondsVisible: true,
//         },
//         pane: 0,
//     };
//     const domElement = document.getElementById('tvchart');
//     const chart = LightweightCharts.createChart(domElement, chartProperties);
//     const candleseries = chart.addCandlestickSeries();
//     const klinedata = await getData();
//     candleseries.setData(klinedata);
//     //SMA
//     const sma_series = chart.addLineSeries({
//         color: 'red',
//         lineWidth: 1
//     });
//     const sma_data = klinedata
//         .filter((d) => d.sma)
//         .map((d) => ({
//             time: d.time,
//             value: d.sma
//         }));
//     sma_series.setData(sma_data);
//     //EMA
//     const ema_series = chart.addLineSeries({
//         color: 'green',
//         lineWidth: 1
//     });
//     const ema_data = klinedata
//         .filter((d) => d.ema)
//         .map((d) => ({
//             time: d.time,
//             value: d.ema
//         }));
//     ema_series.setData(ema_data);
//     //MARKERS
//     candleseries.setMarkers(
//         klinedata
//         .filter((d) => d.long || d.short)
//         .map((d) =>
//             d.long ? {
//                 time: d.time,
//                 position: 'belowBar',
//                 color: 'green',
//                 shape: 'arrowUp',
//                 text: 'LONG',
//             } : {
//                 time: d.time,
//                 position: 'aboveBar',
//                 color: 'red',
//                 shape: 'arrowDown',
//                 text: 'SHORT',
//             }
//         )
//     );
//     //RSI
//     const rsi_series = chart.addLineSeries({
//         color: 'purple',
//         lineWidth: 1,
//         pane: 1,
//     });
//     const rsi_data = klinedata
//         .filter((d) => d.rsi)
//         .map((d) => ({
//             time: d.time,
//             value: d.rsi
//         }));
//     rsi_series.setData(rsi_data);
//     //MACD FAST
//     const macd_fast_series = chart.addLineSeries({
//         color: 'blue',
//         lineWidth: 1,
//         pane: 2,
//     });
//     const macd_fast_data = klinedata
//         .filter((d) => d.macd_fast)
//         .map((d) => ({
//             time: d.time,
//             value: d.macd_fast
//         }));
//     macd_fast_series.setData(macd_fast_data);
//     //MACD SLOW
//     const macd_slow_series = chart.addLineSeries({
//         color: 'red',
//         lineWidth: 1,
//         pane: 2,
//     });
//     const macd_slow_data = klinedata
//         .filter((d) => d.macd_slow)
//         .map((d) => ({
//             time: d.time,
//             value: d.macd_slow
//         }));
//     macd_slow_series.setData(macd_slow_data);
//     //MACD HISTOGRAM
//     const macd_histogram_series = chart.addHistogramSeries({
//         pane: 2,
//     });
//     const macd_histogram_data = klinedata
//         .filter((d) => d.macd_histogram)
//         .map((d) => ({
//             time: d.time,
//             value: d.macd_histogram,
//             color: d.macd_histogram > 0 ? 'green' : 'red',
//         }));
//     macd_histogram_series.setData(macd_histogram_data);
// };

// renderChart();

const {
    log,
    error
} = console;

const getData = async () => {
    const resp = await fetch('http://127.0.0.1:5001/stream');
    const data = await resp.json();
    return data;
};

const renderChart = async () => {
    const chartProperties = {
        timeScale: {
            timeVisible: true,
            secondsVisible: true,
        },
    };

    const domElement = document.getElementById('tvchart');
    const chart = LightweightCharts.createChart(domElement, chartProperties);
    const candleseries = chart.addCandlestickSeries();

    setInterval(async () => {
        const data = await getData();
        candleseries.update(data);

        // Marker logic (adapt based on your signal generation)
        if (data.signal === 1) { // Assuming 1 represents a sell signal
            candleseries.setMarkers([{
                time: data.time,
                position: 'aboveBar',
                color: 'red',
                shape: 'arrowDown',
                text: 'SELL'
            }]);
        } else if (data.signal === 2) { // Assuming 2 represents a buy signal 
            candleseries.setMarkers([{
                time: data.time,
                position: 'belowBar',
                color: 'green',
                shape: 'arrowUp',
                text: 'BUY'
            }]);
        } else {
            candleseries.setMarkers([]); // Clear markers if no signal
        }
    }, 1000); // Fetch data every 1 second
};

renderChart();