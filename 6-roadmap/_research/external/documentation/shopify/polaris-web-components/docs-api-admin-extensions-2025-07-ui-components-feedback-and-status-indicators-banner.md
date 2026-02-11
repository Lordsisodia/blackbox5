---
{
  "fetch": {
    "url": "https://shopify.dev/docs/api/admin-extensions/2025-07/ui-components/feedback-and-status-indicators/banner",
    "fetched_at": "2026-02-10T13:28:29.627766",
    "status": 200,
    "size_bytes": 240385
  },
  "metadata": {
    "title": "Banner",
    "source": "shopify",
    "category": "polaris-web-components",
    "section": "feedback-and-status-indicators",
    "component": "banner"
  }
}
---

# Banner

Choose a version:2026-01 latest2025-10 2025-07 2025-04 2025-01 2024-10 2024-07 2024-04 2024-01 2023-10 2025-07# BannerAsk assistantUse this component if you need to communicate to merchants in a prominent way.

## [Anchor to bannerprops](/docs/api/admin-extensions/2025-07/ui-components/feedback-and-status-indicators/banner#bannerprops)BannerProps[Anchor to dismissible](/docs/api/admin-extensions/2025-07/ui-components/feedback-and-status-indicators/banner#bannerprops-propertydetail-dismissible)dismissible**dismissible**boolean**boolean**Whether or not the banner can be dismissed

[Anchor to id](/docs/api/admin-extensions/2025-07/ui-components/feedback-and-status-indicators/banner#bannerprops-propertydetail-id)id**id**string**string**A unique identifier for the element.

[Anchor to onDismiss](/docs/api/admin-extensions/2025-07/ui-components/feedback-and-status-indicators/banner#bannerprops-propertydetail-ondismiss)onDismiss**onDismiss**() => void**() => void**Function invoked when the banner is dismissed

[Anchor to primaryAction](/docs/api/admin-extensions/2025-07/ui-components/feedback-and-status-indicators/banner#bannerprops-propertydetail-primaryaction)primaryAction**primaryAction**RemoteFragment**RemoteFragment**Sets the Primary action button of the container. This component must be a button component.

[Anchor to secondaryAction](/docs/api/admin-extensions/2025-07/ui-components/feedback-and-status-indicators/banner#bannerprops-propertydetail-secondaryaction)secondaryAction**secondaryAction**RemoteFragment**RemoteFragment**Sets the Secondary action button of the container. This component must be a button component.

[Anchor to title](/docs/api/admin-extensions/2025-07/ui-components/feedback-and-status-indicators/banner#bannerprops-propertydetail-title)title**title**string**string**Message to display inside the banner

[Anchor to tone](/docs/api/admin-extensions/2025-07/ui-components/feedback-and-status-indicators/banner#bannerprops-propertydetail-tone)tone**tone**ToneTone**ToneTone**Adjusts the color and icon of the banner

### Tone```

'info' | 'success' | 'warning' | 'critical'

```ExamplesSimple Banner exampleReactJSCopy9912345678910111213141516import React from 'react';import {  render,  Banner,  Paragraph,} from '@shopify/ui-extensions-react/admin';render('Playground', () => <App />);function App() {  return (    <Banner title="Shipping rates changed" dismissible onDismiss={() => console.log('dismissed banner')}>      <Paragraph>Your store may be affected</Paragraph>    </Banner>  );}## Preview### Examples- #### Simple Banner exampleReact```

import React from 'react';

import {

render,

Banner,

Paragraph,

} from '@shopify/ui-extensions-react/admin';

render('Playground', () => <App />);

function App() {

return (

<Banner title="Shipping rates changed" dismissible onDismiss={() => console.log('dismissed banner')}>

<Paragraph>Your store may be affected</Paragraph>

</Banner>

);

}

```JS```

import {extend, Banner} from '@shopify/ui-extensions/admin';

extend('Playground', (root) => {

const banner = root.createComponent(Banner, {

title: 'Shipping rates changed',

dismissible: true,

onDismiss: () => console.log('dismissed banner')

}, 'Your store may be affected');

root.appendChild(banner);

});

```Was this page helpful?YesNo### Updates- [Developer changelog](/changelog)- [Shopify Editions](https://www.shopify.com/editions)### Business growth- [Shopify Partners Program](https://www.shopify.com/partners?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Shopify App Store](https://apps.shopify.com/?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Shopify Academy](https://www.shopifyacademy.com/page/catalog#role_developer?utm_source=web_dotdev&utm_medium=footer_businessgrowth)### Legal- [Terms of service](https://www.shopify.com/legal/terms?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [API terms of use](https://www.shopify.com/legal/api-terms?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Privacy policy](https://www.shopify.com/legal/privacy?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Partners Program Agreement](https://www.shopify.com/partners/terms?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)### Shopify- [About Shopify](https://www.shopify.com/about?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Shopify Plus](https://www.shopify.com/plus?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Careers](https://www.shopify.com/careers?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Investors](https://investors.shopify.com/home/default.aspx?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Press and media](https://shopify.com/news?shpxid=7db0d4e4-24E8-4087-58FA-7EE470CA745A)