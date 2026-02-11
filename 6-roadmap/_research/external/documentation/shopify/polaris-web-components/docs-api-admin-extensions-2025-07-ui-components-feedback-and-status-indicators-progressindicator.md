---
{
  "fetch": {
    "url": "https://shopify.dev/docs/api/admin-extensions/2025-07/ui-components/feedback-and-status-indicators/progressindicator",
    "fetched_at": "2026-02-10T13:28:30.963994",
    "status": 200,
    "size_bytes": 239546
  },
  "metadata": {
    "title": "ProgressIndicator",
    "source": "shopify",
    "category": "polaris-web-components",
    "section": "feedback-and-status-indicators",
    "component": "progressindicator"
  }
}
---

# ProgressIndicator

Choose a version:2026-01 latest2025-10 2025-07 2025-04 2025-01 2024-10 2024-07 2024-04 2024-01 2023-10 2025-07# ProgressIndicatorAsk assistantUse this component to notify merchants that their action is being processed or loaded.

## [Anchor to progressindicatorprops](/docs/api/admin-extensions/2025-07/ui-components/feedback-and-status-indicators/progressindicator#progressindicatorprops)ProgressIndicatorProps[Anchor to size](/docs/api/admin-extensions/2025-07/ui-components/feedback-and-status-indicators/progressindicator#progressindicatorprops-propertydetail-size)size**size**SizeScaleSizeScale**SizeScaleSizeScale**required**required**The size of the component.

[Anchor to accessibilityLabel](/docs/api/admin-extensions/2025-07/ui-components/feedback-and-status-indicators/progressindicator#progressindicatorprops-propertydetail-accessibilitylabel)accessibilityLabel**accessibilityLabel**string**string**A label that describes the purpose or contents of the element. When set, it will be announced to users using assistive technologies and will provide them with more context. When set, any children or `label` supplied will not be announced to screen readers.

[Anchor to id](/docs/api/admin-extensions/2025-07/ui-components/feedback-and-status-indicators/progressindicator#progressindicatorprops-propertydetail-id)id**id**string**string**A unique identifier for the element.

[Anchor to tone](/docs/api/admin-extensions/2025-07/ui-components/feedback-and-status-indicators/progressindicator#progressindicatorprops-propertydetail-tone)tone**tone**'inherit' | 'default'**'inherit' | 'default'**Default: 'default'**Default: 'default'**Set the color of the progress indicator.

- `inherit` will take the color value from its parent, giving the progress indicator a monochrome appearance.

[Anchor to variant](/docs/api/admin-extensions/2025-07/ui-components/feedback-and-status-indicators/progressindicator#progressindicatorprops-propertydetail-variant)variant**variant**'spinner'**'spinner'**Default: 'spinner'**Default: 'spinner'**Style of the progress indicator

### SizeScale```

'small-300' | 'small-200' | 'small-100' | 'base' | 'large-100' | 'large-200' | 'large-300'

```ExamplesSimple spinner exampleReactJSCopy99123456789101112import {  reactExtension,  ProgressIndicator,} from '@shopify/ui-extensions-react/admin';reactExtension('Playground', () => <App />);function App() {  return (    <ProgressIndicator size="small-200" />  );}## Preview### Examples- #### Simple spinner exampleReact```

import {

reactExtension,

ProgressIndicator,

} from '@shopify/ui-extensions-react/admin';

reactExtension('Playground', () => <App />);

function App() {

return (

<ProgressIndicator size="small-200" />

);

}

```JS```

import {

extension,

ProgressIndicator,

} from '@shopify/ui-extensions/admin';

export default extension(

'Playground',

(root) => {

const progressIndicator = root.createComponent(

ProgressIndicator,

{

size: 'small-200',

},

);

root.appendChild(progressIndicator);

},

);

```## [Anchor to related](/docs/api/admin-extensions/2025-07/ui-components/feedback-and-status-indicators/progressindicator#related)Related[ButtonButton](/docs/api/admin-extensions/components/actions/button)[ - Button](/docs/api/admin-extensions/components/actions/button)Was this page helpful?YesNo### Updates- [Developer changelog](/changelog)- [Shopify Editions](https://www.shopify.com/editions)### Business growth- [Shopify Partners Program](https://www.shopify.com/partners?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Shopify App Store](https://apps.shopify.com/?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Shopify Academy](https://www.shopifyacademy.com/page/catalog#role_developer?utm_source=web_dotdev&utm_medium=footer_businessgrowth)### Legal- [Terms of service](https://www.shopify.com/legal/terms?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [API terms of use](https://www.shopify.com/legal/api-terms?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Privacy policy](https://www.shopify.com/legal/privacy?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Partners Program Agreement](https://www.shopify.com/partners/terms?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)### Shopify- [About Shopify](https://www.shopify.com/about?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Shopify Plus](https://www.shopify.com/plus?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Careers](https://www.shopify.com/careers?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Investors](https://investors.shopify.com/home/default.aspx?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Press and media](https://shopify.com/news?shpxid=7db0d4e4-24E8-4087-58FA-7EE470CA745A)