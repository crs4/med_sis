# Diamond-React
https://doodle.com/group-poll/participate/elEvogla
https://medium.com/analytics-vidhya/integrating-a-machine-learning-model-with-django-79dd47eabef1


This is a [Next.js](https://nextjs.org/) project bootstrapped with [`create-next-app`](https://github.com/vercel/next.js/tree/canary/packages/create-next-app).

## Getting Started

First, run the development server:

```bash
npm run dev
# or
yarn dev
```

Open [http://localhost:3000](http://localhost:3000) with your browser to see the result.

You can start editing the page by modifying `pages/index.js`. The page auto-updates as you edit the file.

[API routes](https://nextjs.org/docs/api-routes/introduction) can be accessed on [http://localhost:3000/api/hello](http://localhost:3000/api/hello). This endpoint can be edited in `pages/api/hello.js`.

The `pages/api` directory is mapped to `/api/*`. Files in this directory are treated as [API routes](https://nextjs.org/docs/api-routes/introduction) instead of React pages.

## Learn More

To learn more about Next.js, take a look at the following resources:

- [Next.js Documentation](https://nextjs.org/docs) - learn about Next.js features and API.
- [Learn Next.js](https://nextjs.org/learn) - an interactive Next.js tutorial.

You can check out [the Next.js GitHub repository](https://github.com/vercel/next.js/) - your feedback and contributions are welcome!

## Deploy on Vercel

The easiest way to deploy your Next.js app is to use the [Vercel Platform](https://vercel.com/new?utm_medium=default-template&filter=next.js&utm_source=create-next-app&utm_campaign=create-next-app-readme) from the creators of Next.js.

Check out our [Next.js deployment documentation](https://nextjs.org/docs/deployment) for more details.
# diamond-next

Section =======
ProfileGeneral
LandformTopography
ClimateAndWeather
LandUse - Cultivated - NotCultivated
LitterLayer
Surface
SurfaceCracks
CoarseFragments
SurfaceUnevenness
Section =======

Layer Section =======




Filters
step 1: create S4M_Filter
- chose extends (sections) 
- chhose type ( mapping )
- choose fields (mapping) max 20
step 2: create rules for each field
- for each field
    - set match : ANY, ALL
    - add rules ( type, value)
step 3: test apply
 - API GET data with  filters  (profiles/, samples/) 
 - View map and table ( id, lat, lon added)
 - SAVE FILTER, SAVE FILTER + PUBLISH new GEONODE LAYER 
step 4: 
 - RESULT new FILTER
 - RESULT new GEONODE LAYER

new models: filter, s4m_dataset


mapping -> forms + save su model 







S4M_filter:
{
    mapping: type
    extends: [fieldnames] use sections
    filters: [
        {
            fieldname : -----,
            match : ANY,ALL (or/and),
            rules : [{
                type   : type,
                value  : ----,
            }],
        }
    ]
}
(max 20 fields)


subsetFields  legare agli ids mapping , array 
rules array di rule  
[(, AND, OR,), NOT]
type profile/samples, general(+classification),layer,label data,

s4m_dataset:
geonode_id
filetr_id
