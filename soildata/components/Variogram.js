import React, { useState, useEffect } from 'react';
import { Chart } from 'primereact/chart';

const VariogramGraph = ( { data } ) => {
    const [chartData, setChartData] = useState({});
    const [chartOptions, setChartOptions] = useState({});
    const [variogram, setVariogram] = useState(data)
    
    useEffect(() => {
        if ( !data )
            return
        // 2. Generates the Sample Variogram Points (Experimental)
        // x = lag distance, y = semi-variance
        const experimentalPoints = data.var_pts;
        // 3. Generate Fitted Model Curve (Theoretical)
        const modelCurve = data.mod_pts;
        // 4. Chart.js Data Structure
        const myData = {
            datasets: [
                {
                    type: 'scatter',
                    label: 'Experimental Variogram',
                    data: experimentalPoints,
                    backgroundColor: '#3B82F6',
                    borderColor: '#1E40AF',
                    pointRadius: 6,
                    showLine: false
                },
                {
                    type: 'line',
                    label: 'Fitted Model ('+data.model+')',
                    data: modelCurve,
                    borderColor: '#EF4444',
                    borderWidth: 2,
                    fill: false,
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
                    title: { display: true, text: 'Distance Lag (m)', font: { weight: 'bold' } },
                    min: variogram.mind - 5 ,
                    max: variogram.maxd + 5
                },
                y: {
                    title: { display: true, text: 'Semi-variance', font: { weight: 'bold' } },
                    min: -5,
                    max: variogram.max + 5
                }
            },
            plugins: {
                title: {
                    display: true,
                    text: 'Semi Variogram',
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

export default VariogramGraph;