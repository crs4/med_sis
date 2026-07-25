import React, { useState, useEffect } from 'react';
import { Chart } from 'primereact/chart';

const PtfGraph = ( { data } ) => {
    const [chartData, setChartData] = useState({});
    const [chartOptions, setChartOptions] = useState({});
    const [ptfData, setPtfData] = useState(data)
    
    useEffect(() => {
        if ( !data )
            return
        // 1. Generates the Curve from Points 
        //  x = matrix potential (kPa), y = volumetric water content (cm^3.cm^-3)
        const modelCurve = data.pts;
        // 2. Chart.js Data Structure
        const myData = {
            datasets: [
                {
                    type: 'line',
                    label: 'Water Retention Curve',
                    data: modelCurve,
                    borderColor: '#5844ef',
                    borderWidth: 2,
                    fill: false,
                    cubicInterpolationMode: 'monotone',
                    tension: 0.1,
                    pointRadius: 0 // Hides points to make it a smooth line
                }
            ]
        };

        // 5. Chart.js Options
        const options = {
            responsive: true,
            maintainAspectRatio: false,
            aspectRatio: 0.6,
            scales: {
                x: {
                    title: { display: true, text: 'Matrix potential (kPa) absolute value', font: { weight: 'bold' } },
                    min: 1 ,
                    max: 1500 
                },
                y: {
                    title: { display: true, text: 'Volumetric Water Content (cm^3.cm^-3)', font: { weight: 'bold' } },
                    min: 0,
                    max: 2 * ptfData.max 
                }
            },
            plugins: {
                title: {
                    display: true,
                    text: 'Water Retention Curve',
                    font: { size: 16 }
                }
            }
        };

        setChartData(myData);
        setChartOptions(options);
    }, [data] ); // eslint-disable-line

    return (
        <Chart type="scatter" data={chartData} options={chartOptions} style={{ width: '100%', height: '500px' }} />
    );
};

export default PtfGraph;