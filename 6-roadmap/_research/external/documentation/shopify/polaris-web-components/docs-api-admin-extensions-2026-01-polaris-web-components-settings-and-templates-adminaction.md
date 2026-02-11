---
{
  "fetch": {
    "url": "https://shopify.dev/docs/api/admin-extensions/2026-01/polaris-web-components/settings-and-templates/adminaction",
    "fetched_at": "2026-02-10T13:30:52.391101",
    "status": 200,
    "size_bytes": 236342
  },
  "metadata": {
    "title": "AdminAction",
    "source": "shopify",
    "category": "polaris-web-components",
    "section": "settings-and-templates",
    "component": "adminaction"
  }
}
---

# AdminAction

Choose a version:2026-01 latest2025-10 2025-07 2025-04 2025-01 2024-10 2024-07 2024-04 2024-01 2023-10 2026-01latest# AdminActionAsk assistantUse `s-admin-action` to configure a primary and secondary action and title. Use of this component is required in order to use Admin action extensions.

## [Anchor to properties](/docs/api/admin-extensions/latest/polaris-web-components/settings-and-templates/adminaction#properties)Properties[Anchor to heading](/docs/api/admin-extensions/latest/polaris-web-components/settings-and-templates/adminaction#properties-propertydetail-heading)heading**heading**string**string**The text to use as the Action modal’s title. If not provided, the name of the extension will be used.

[Anchor to loading](/docs/api/admin-extensions/latest/polaris-web-components/settings-and-templates/adminaction#properties-propertydetail-loading)loading**loading**boolean**boolean**Default: false**Default: false**Whether the action is in a loading state, such as initial page load or action opening. When true, the action could be in an inert state, which prevents user interaction.

## [Anchor to slots](/docs/api/admin-extensions/latest/polaris-web-components/settings-and-templates/adminaction#slots)Slots[Anchor to primary-action](/docs/api/admin-extensions/latest/polaris-web-components/settings-and-templates/adminaction#slots-propertydetail-primaryaction)primary-action**primary-action**HTMLElement**HTMLElement**The primary action to display in the admin action.

[Anchor to secondary-actions](/docs/api/admin-extensions/latest/polaris-web-components/settings-and-templates/adminaction#slots-propertydetail-secondaryactions)secondary-actions**secondary-actions**HTMLElement**HTMLElement**The secondary actions to display in the admin action.

ExamplesExample## jsx Copy99123456789101112131415<s-admin-action title="My App Action">  Modal content  <s-button    slot="primary-action"    onClick={() => console.log('pressed primary action')}  >    Primary  </s-button>  <s-button    slot="secondary-actions"    onClick={() => console.log('pressed secondary action')}  >    Secondary  </s-button></s-admin-action>;## Preview### Examples- #### jsx```

<s-admin-action title="My App Action">

Modal content

<s-button

slot="primary-action"

onClick={() => console.log('pressed primary action')}

>

Primary

</s-button>

<s-button

slot="secondary-actions"

onClick={() => console.log('pressed secondary action')}

>

Secondary

</s-button>

</s-admin-action>;

```Was this page helpful?YesNo### Updates- [Developer changelog](/changelog)- [Shopify Editions](https://www.shopify.com/editions)### Business growth- [Shopify Partners Program](https://www.shopify.com/partners?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Shopify App Store](https://apps.shopify.com/?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Shopify Academy](https://www.shopifyacademy.com/page/catalog#role_developer?utm_source=web_dotdev&utm_medium=footer_businessgrowth)### Legal- [Terms of service](https://www.shopify.com/legal/terms?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [API terms of use](https://www.shopify.com/legal/api-terms?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Privacy policy](https://www.shopify.com/legal/privacy?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Partners Program Agreement](https://www.shopify.com/partners/terms?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)### Shopify- [About Shopify](https://www.shopify.com/about?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Shopify Plus](https://www.shopify.com/plus?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Careers](https://www.shopify.com/careers?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Investors](https://investors.shopify.com/home/default.aspx?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Press and media](https://shopify.com/news?shpxid=7db0d4e4-24E8-4087-58FA-7EE470CA745A)