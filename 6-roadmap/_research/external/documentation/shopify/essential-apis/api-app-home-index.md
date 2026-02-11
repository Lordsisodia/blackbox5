---
{
  "fetch": {
    "url": "https://shopify.dev/api/app-home/index",
    "fetched_at": "2026-02-10T13:40:05.095212",
    "status": 200,
    "size_bytes": 415865
  },
  "metadata": {
    "title": "App home",
    "source": "shopify",
    "category": "polaris-web-components",
    "section": "app-home",
    "component": "index"
  }
}
---

# App home

# App homeThe [app home](/docs/apps/admin/embedded-app-home) is the primary surface merchants use to interact with your app. It displays your app's interface in the Shopify admin and provides access to merchant data using Shopify's APIs. With Polaris components and App Bridge, you can build performant apps using familiar web technologies.Ask assistant

## [Anchor to Getting started](/docs/api/app-home/index#getting-started)Getting startedTo build for the App Home we recommend adding App Bridge and the Polaris Web Components to your application.Polaris web components provide a consistent UI experience that matches the Shopify Admin while leveraging standard web platform features. To use these components in your app, you need to include the Polaris script in your application.Apps that use these components can also include pre-built UI [patterns](/docs/api/app-home/patterns) that are implemented using Polaris web components. These patterns help you quickly build consistent, familiar experiences for merchants that follow Shopify's design guidelines.New React Router Application

Start building your app fast with the Shopify CLI and the [Shopify React Router App template](https://github.com/Shopify/shopify-app-template-react-router). The CLI will set up App Bridge and the Polaris Web Components for you.You will need to select:

- Select Build a React Router app (recommended)

- Select JavaScript OR TypeScript.

Existing Remix Application

Add the Polaris Web Components script tag to your `app/root.tsx` file's `<head>`.To use the Remix router you will need to control the custom event `shopify:navigate` and push that into `useNavigate`.Build your own way

When building your own way add the script tag right after the existing App Bridge script tag in your HTML head.## SetupCopy91shopify app init## SetupCopy99123456789101112131415161718192021222324252627import {useNavigate} from '@remix-run/react';export default function App() {  const navigate = useNavigate();  useEffect(() => {    const handleNavigate = (event) => {      const href = event.target.getAttribute('href');      if (href) navigate(href);    };    document.addEventListener('shopify:navigate', handleNavigate);    return () => {      document.removeEventListener('shopify:navigate', handleNavigate);    };  }, [navigate]);  return (    <html>      <head>        ...        <script src="https://cdn.shopify.com/shopifycloud/polaris.js"></script>      </head>      ...    </html>  );}## SetupCopy912345<head>  <meta name="shopify-api-key" content="%SHOPIFY_API_KEY%" />  <script src="https://cdn.shopify.com/shopifycloud/app-bridge.js"></script>  <script src="https://cdn.shopify.com/shopifycloud/polaris.js"></script></head>

## [Anchor to Resources](/docs/api/app-home/index#resources)Resources[Polaris web componentsView all available componentsPolaris web componentsView all available components](/docs/api/app-home/polaris-web-components)[Polaris web componentsView all available components](/docs/api/app-home/polaris-web-components)[PatternsCommon app home patternsPatternsCommon app home patterns](/docs/api/app-home/patterns)[PatternsCommon app home patterns](/docs/api/app-home/patterns)[StorybookExplore component examplesStorybookExplore component examples](https://storybook.polaris-admin.shopify.dev/)[StorybookExplore component examples](https://storybook.polaris-admin.shopify.dev/)[App Design GuidelinesFollow our UX guidelines when you're designing your app to ensure that they're predictable and easy to use.App Design GuidelinesFollow our UX guidelines when you're designing your app to ensure that they're predictable and easy to use.](https://shopify.dev/docs/apps/design-guidelines)[App Design GuidelinesFollow our UX guidelines when you're designing your app to ensure that they're predictable and easy to use.](https://shopify.dev/docs/apps/design-guidelines)[Shopify CLI and Tools forumVisit our Shopify CLI and Tools forum if you need help using Shopify App Bridge.Shopify CLI and Tools forumVisit our Shopify CLI and Tools forum if you need help using Shopify App Bridge.](https://community.shopify.com/c/shopify-cli-and-tools/bd-p/tools)[Shopify CLI and Tools forumVisit our Shopify CLI and Tools forum if you need help using Shopify App Bridge.](https://community.shopify.com/c/shopify-cli-and-tools/bd-p/tools)[Figma KitDownload the Figma KitFigma KitDownload the Figma Kit](https://www.figma.com/community/file/1554895871000783188/polaris-ui-kit-community)[Figma KitDownload the Figma Kit](https://www.figma.com/community/file/1554895871000783188/polaris-ui-kit-community)

## [Anchor to Your first API call](/docs/api/app-home/index#your-first-api-call)Your first API callThe following example uses [`Resource Picker`](https://shopify.dev/docs/api/app-home/apis/resource-picker) to open a UI component that enables users to browse, find, and select products from their store using a familiar experiences.## Resource PickerCopy99123456789101112131415161718<!DOCTYPE html><head>  <meta name="shopify-api-key" content="%SHOPIFY_API_KEY%" />  <script src="https://cdn.shopify.com/shopifycloud/app-bridge.js"></script></head><body>  <button id="open-picker">Open resource picker</button>  <script>    document      .getElementById('open-picker')      .addEventListener('click', async () => {        const selected = await shopify.resourcePicker({type: 'product'});        console.log(selected);      });  </script></body>

## [Anchor to TypeScript](/docs/api/app-home/index#typescript)TypeScriptShopify App Bridge provides a companion npm library for TypeScript types, available at [`@shopify/app-bridge-types`](https://www.npmjs.com/package/@shopify/app-bridge-types).If you're using the [React library](/docs/api/app-home#react), then the types package is already included.Additionally, Shopify provides a companion npm library for Polaris web components types, available at [`@shopify/polaris-types`](https://www.npmjs.com/package/@shopify/polaris-types).App Bridge Installation

The `@shopify/app-bridge-types` package can be installed using `yarn` or `npm`.App Bridge Configuration

Adding the `@shopify/app-bridge-types` package to your `tsconfig.json` file will enable type checking for all files in your project.Polaris Web Components Installation

The `@shopify/polaris-types` package can be installed using `yarn` or `npm`. Specify `latest` in package.json if using [https://cdn.shopify.com/shopifycloud/polaris.js](https://cdn.shopify.com/shopifycloud/polaris.js).Polaris Web Components Configuration

Adding the `@shopify/polaris-types` package to your `tsconfig.json` file will enable type checking for all files in your project.## InstallationnpmyarnCopy91npm install --save-dev @shopify/app-bridge-types91yarn add --dev @shopify/app-bridge-typesnpm```

npm install --save-dev @shopify/app-bridge-types

```yarn```

yarn add --dev @shopify/app-bridge-types

```## ConfigurationCopy## tsconfig.json912345{  "compilerOptions": {    "types": ["@shopify/app-bridge-types"]  }}## Installationnpmyarnpackage.jsonCopy91npm install --save-dev @shopify/polaris-types91yarn add --dev @shopify/polaris-types912345{  "devDependencies": {    "@shopify/polaris-types": "latest"  }}npm```

npm install --save-dev @shopify/polaris-types

```yarn```

yarn add --dev @shopify/polaris-types

```package.json```

{

"devDependencies": {

"@shopify/polaris-types": "latest"

}

}

```## ConfigurationCopy## tsconfig.json912345{  "compilerOptions": {    "types": ["@shopify/polaris-types"]  }}

## [Anchor to Global variable](/docs/api/app-home/index#global-variable)Global variableAfter App Bridge is set up in your app, you have access to the `shopify` global variable. This variable exposes various App Bridge functionalities, such as [displaying toast notifications](/docs/api/app-home/apis/toast) or [retrieving app configuration details](/docs/api/app-home/apis/config).To explore all the functionality available on the `shopify` global variable:

-

Open the Chrome developer console while in the Shopify admin.

-

Switch the frame context to your app's `iframe`.

-

Enter `shopify` in the console.

## [Anchor to Direct API access](/docs/api/app-home/index#direct-api-access)Direct API accessYou can make requests to the Admin API directly from your app using the standard [web `fetch` API](https://developer.mozilla.org/en-US/docs/Web/API/fetch)!Any `fetch()` calls from your app to Shopify's Admin GraphQL API are automatically authenticated by default. These calls are fast too, because Shopify handles requests directly.Direct API access is disabled by default. It can be [enabled](/docs/apps/tools/cli/configuration#admin) in your app TOML file, along with whether you want to use direct API access with [online access](/docs/apps/auth/oauth/access-modes#online-access) or [offline access](/docs/apps/auth/oauth/access-modes#offline-access) mode.[Learn more about API access modesConfiguration guideLearn more about API access modesConfiguration guide](/docs/apps/tools/cli/configuration)[Learn more about API access modes - Configuration guide](/docs/apps/tools/cli/configuration)## Query Shopify dataCopy## Fetch directly from the Admin API9912345678910111213141516const res = await fetch('shopify:admin/api/2025-04/graphql.json', {  method: 'POST',  body: JSON.stringify({    query: `      query GetProduct($id: ID!) {        product(id: $id) {          title        }      }    `,    variables: {id: 'gid://shopify/Product/1234567890'},  }),});const {data} = await res.json();console.log(data);

## [Anchor to Migration](/docs/api/app-home/index#migration)MigrationIf you have an app that uses components and hooks from Shopify App Bridge React 3.x.x, then you can follow the [migration guide](/docs/api/app-bridge/migration-guide) to upgrade your components and hooks to the latest version.

## [Anchor to Next steps](/docs/api/app-home/index#next-steps)Next stepsNow that you've initialized your app, you can use any [Shopify App Bridge features](/docs/api/app-home/apis).SupportIf you need help using Shopify App Bridge, please visit our [App Bridge community forum](https://community.shopify.dev/c/app-bridge). It is the best place to discuss libraries and get support.**Support:** If you need help using Shopify App Bridge, please visit our [App Bridge community forum](https://community.shopify.dev/c/app-bridge). It is the best place to discuss libraries and get support.

Was this page helpful?YesNo### Updates- [Developer changelog](/changelog)- [Shopify Editions](https://www.shopify.com/editions)### Business growth- [Shopify Partners Program](https://www.shopify.com/partners?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Shopify App Store](https://apps.shopify.com/?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Shopify Academy](https://www.shopifyacademy.com/page/catalog#role_developer?utm_source=web_dotdev&utm_medium=footer_businessgrowth)### Legal- [Terms of service](https://www.shopify.com/legal/terms?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [API terms of use](https://www.shopify.com/legal/api-terms?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Privacy policy](https://www.shopify.com/legal/privacy?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Partners Program Agreement](https://www.shopify.com/partners/terms?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)### Shopify- [About Shopify](https://www.shopify.com/about?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Shopify Plus](https://www.shopify.com/plus?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Careers](https://www.shopify.com/careers?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Investors](https://investors.shopify.com/home/default.aspx?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Press and media](https://shopify.com/news?shpxid=7db0d4e4-24E8-4087-58FA-7EE470CA745A)