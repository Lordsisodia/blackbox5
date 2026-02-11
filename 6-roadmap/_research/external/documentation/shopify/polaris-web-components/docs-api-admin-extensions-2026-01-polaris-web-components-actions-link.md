---
{
  "fetch": {
    "url": "https://shopify.dev/docs/api/admin-extensions/2026-01/polaris-web-components/actions/link",
    "fetched_at": "2026-02-10T13:29:27.711724",
    "status": 200,
    "size_bytes": 300126
  },
  "metadata": {
    "title": "Link",
    "source": "shopify",
    "category": "polaris-web-components",
    "section": "actions",
    "component": "link"
  }
}
---

# Link

Choose a version:2026-01 latest2025-10 2025-07 2025-04 2025-01 2024-10 2024-07 2024-04 2024-01 2023-10 2026-01latest# LinkAsk assistantMakes text interactive, allowing users to navigate to other pages or perform specific actions. Supports standard URLs, custom protocols, and navigation within Shopify or app pages.

## [Anchor to properties](/docs/api/admin-extensions/latest/polaris-web-components/actions/link#properties)Properties[Anchor to accessibilityLabel](/docs/api/admin-extensions/latest/polaris-web-components/actions/link#properties-propertydetail-accessibilitylabel)accessibilityLabel**accessibilityLabel**string**string**A label that describes the purpose or contents of the Link. It will be read to users using assistive technologies such as screen readers.

Use this when using only an icon or the content of the link is not enough context for users using assistive technologies.

[Anchor to command](/docs/api/admin-extensions/latest/polaris-web-components/actions/link#properties-propertydetail-command)command**command**'--auto' | '--show' | '--hide' | '--toggle'**'--auto' | '--show' | '--hide' | '--toggle'**Default: '--auto'**Default: '--auto'**Sets the action the [command](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/button#command) should take when this clickable is activated.

See the documentation of particular components for the actions they support.

- `--auto`: a default action for the target component.

- `--show`: shows the target component.

- `--hide`: hides the target component.

- `--toggle`: toggles the target component.

[Anchor to commandFor](/docs/api/admin-extensions/latest/polaris-web-components/actions/link#properties-propertydetail-commandfor)commandFor**commandFor**string**string**Sets the element the [commandFor](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/button#commandfor) should act on when this clickable is activated.

[Anchor to download](/docs/api/admin-extensions/latest/polaris-web-components/actions/link#properties-propertydetail-download)download**download**string**string**Causes the browser to treat the linked URL as a download with the string being the file name. Download only works for same-origin URLs or the `blob:` and `data:` schemes.

[Anchor to href](/docs/api/admin-extensions/latest/polaris-web-components/actions/link#properties-propertydetail-href)href**href**string**string**The URL to link to.

- If set, it will navigate to the location specified by `href` after executing the `click` event.

- If a `commandFor` is set, the `command` will be executed instead of the navigation.

[Anchor to interestFor](/docs/api/admin-extensions/latest/polaris-web-components/actions/link#properties-propertydetail-interestfor)interestFor**interestFor**string**string**Sets the element the [interestFor](https://open-ui.org/components/interest-invokers.explainer/#the-pitch-in-code) should act on when this clickable is activated.

[Anchor to lang](/docs/api/admin-extensions/latest/polaris-web-components/actions/link#properties-propertydetail-lang)lang**lang**string**string**Indicate the text language. Useful when the text is in a different language than the rest of the page. It will allow assistive technologies such as screen readers to invoke the correct pronunciation. [Reference of values](https://www.iana.org/assignments/language-subtag-registry/language-subtag-registry) ("subtag" label)

[Anchor to target](/docs/api/admin-extensions/latest/polaris-web-components/actions/link#properties-propertydetail-target)target**target**"auto" | AnyStringAnyString | "_blank" | "_self" | "_parent" | "_top"**"auto" | AnyStringAnyString | "_blank" | "_self" | "_parent" | "_top"**Default: 'auto'**Default: 'auto'**Specifies where to display the linked URL.

[Anchor to tone](/docs/api/admin-extensions/latest/polaris-web-components/actions/link#properties-propertydetail-tone)tone**tone**"critical" | "auto" | "neutral"**"critical" | "auto" | "neutral"**Default: 'auto'**Default: 'auto'**Sets the tone of the Link, based on the intention of the information being conveyed.

### AnyStringPrevents widening string literal types in a union to `string`.```

string & {}

```## [Anchor to events](/docs/api/admin-extensions/latest/polaris-web-components/actions/link#events)EventsLearn more about [registering events](/docs/api/app-home/using-polaris-components#event-handling).

[Anchor to click](/docs/api/admin-extensions/latest/polaris-web-components/actions/link#events-propertydetail-click)click**click**CallbackEventListenerCallbackEventListener<TTagName> | null**CallbackEventListenerCallbackEventListener<TTagName> | null**### CallbackEventListener```

(EventListener & {

(event: CallbackEvent<T>): void;

}) | null

```### CallbackEvent```

Event & {

currentTarget: HTMLElementTagNameMap[T];

}

```## [Anchor to slots](/docs/api/admin-extensions/latest/polaris-web-components/actions/link#slots)Slots[Anchor to children](/docs/api/admin-extensions/latest/polaris-web-components/actions/link#slots-propertydetail-children)children**children**HTMLElement**HTMLElement**The content of the Link.

ExamplesCodejsxhtmlCopy91<s-link href="javascript:void(0)">fufilling orders</s-link>## Preview### Examples- #### Codejsx```

<s-link href="javascript:void(0)">fufilling orders</s-link>

```html```

<s-link href="#beep">fufilling orders</s-link>

```- #### Basic Links in ParagraphDescriptionLinks automatically inherit the tone from their surrounding paragraph context.jsx```

<s-paragraph>

Your product catalog is empty. Start by <s-link href="javascript:void(0)">adding your first product</s-link> or <s-link href="javascript:void(0)">importing existing inventory</s-link>.

</s-paragraph>

```html```

<s-paragraph>

Your product catalog is empty. Start by <s-link href="javascript:void(0)">adding your first product</s-link> or <s-link href="javascript:void(0)">importing existing inventory</s-link>.

</s-paragraph>

```- #### Links in Subdued ParagraphDescriptionDemonstrates links within subdued paragraph, showing how links can be used in less prominent paragraph contexts for additional guidance or support.jsx```

<s-paragraph color="subdued">

Need help setting up shipping rates? <s-link>View shipping guide</s-link> or <s-link>contact merchant support</s-link>.

</s-paragraph>

```html```

<s-paragraph color="subdued">

Need help setting up shipping rates? <s-link href="javascript:void(0)" target="_blank">View shipping guide</s-link> or <s-link href="javascript:void(0)">contact merchant support</s-link>.

</s-paragraph>

```- #### Critical Context LinksDescriptionIllustrates how links can be used in critical or urgent text contexts, drawing attention to important actions that require immediate user intervention.jsx```

<s-paragraph tone="critical">

Your store will be suspended in 24 hours due to unpaid balance. <s-link href="javascript:void(0)">Update payment method</s-link> to avoid service interruption.

</s-paragraph>

```html```

<s-paragraph tone="critical">

Your store will be suspended in 24 hours due to unpaid balance. <s-link href="javascript:void(0)">Update payment method</s-link> to avoid service interruption.

</s-paragraph>

```- #### Links with Auto ToneDescriptionShows how links automatically adapt their tone to the surrounding text context, maintaining visual consistency while providing navigation.jsx```

<s-paragraph>

You have 15 pending orders to fulfill. <s-link href="javascript:void(0)">Review unfulfilled orders</s-link> to keep customers happy.

</s-paragraph>

```html```

<s-paragraph>

You have 15 pending orders to fulfill. <s-link href="javascript:void(0)">Review unfulfilled orders</s-link> to keep customers happy.

</s-paragraph>

```- #### Links in BannerDescriptionDemonstrates how links can be integrated within banner components to highlight important information and provide direct action paths.jsx```

<s-banner tone="info">

<s-paragraph>

Black Friday campaigns are now available!  <s-link href="javascript:void(0)">Create your campaign</s-link>

</s-paragraph>

</s-banner>

```html```

<s-banner tone="info">

<s-paragraph>

Black Friday campaigns are now available!

<s-link href="javascript:void(0)">Create your campaign</s-link>

</s-paragraph>

</s-banner>

```- #### Links in Box ContainerDescriptionIllustrates using links within a box container to provide contextual navigation and additional information in a visually contained area.jsx```

<s-box padding="base" background="base" borderWidth="base" borderColor="base">

<s-paragraph>

Boost your store's conversion with professional themes. <s-link href="javascript:void(0)">Browse theme store</s-link> or <s-link href="javascript:void(0)">customize your current theme</s-link>.

</s-paragraph>

</s-box>

```html```

<s-box padding="base" background="base" borderWidth="base" borderColor="base">

<s-paragraph>

Boost your store's conversion with professional themes. <s-link href="javascript:void(0)">Browse theme store</s-link> or <s-link href="javascript:void(0)">customize your current theme</s-link>.

</s-paragraph>

</s-box>

```- #### Links in Banner ContextDescriptionShows how links can be used within warning banners to provide immediate actions related to critical notifications.jsx```

<s-banner tone="warning">

<s-paragraph>

Your inventory for "Vintage t-shirt" is running low (3 remaining).  <s-link>Restock inventory</s-link>

</s-paragraph>

</s-banner>

```html```

<s-banner tone="warning">

<s-paragraph>

Your inventory for "Vintage t-shirt" is running low (3 remaining). <s-link>Restock inventory</s-link>

</s-paragraph>

</s-banner>

```- #### Download LinksDescriptionDemonstrates how to create links that trigger file downloads, useful for exporting data or providing downloadable resources.jsx```

<s-paragraph>

Export your customer data for marketing analysis. <s-link href="javascript:void(0)" download="customer-export.csv">Download customer list</s-link>

</s-paragraph>

```html```

<s-paragraph>

Export your customer data for marketing analysis. <s-link href="javascript:void(0)" download="customer-export.csv">Download customer list</s-link>

</s-paragraph>

```- #### External LinksDescriptionIllustrates linking to external resources with different targets, showing how to open links in new tabs and provide navigation to external documentation.jsx```

<s-box padding="base">

<s-paragraph>

Need help with policies? Read our <s-link href="javascript:void(0)" target="_blank">billing docs</s-link> or review the <s-link href="javascript:void(0)" target="_blank">terms of service</s-link>.

</s-paragraph>

</s-box>

```html```

<s-box padding="base">

<s-paragraph>

Need help with policies? Read our <s-link href="javascript:void(0)" target="_blank">billing docs</s-link> or review the <s-link href="javascript:void(0)" target="_blank">terms of service</s-link>.

</s-paragraph>

</s-box>

```- #### Links with Language AttributeDescriptionShows how to use the `lang` attribute to specify the language of a link, supporting internationalization and proper screen reader pronunciation.jsx```

<s-paragraph>

Voir en français: <s-link lang="fr">Gérer les produits</s-link>

</s-paragraph>

```html```

<s-paragraph>

Voir en français: <s-link lang="fr">Gérer les produits</s-link>

</s-paragraph>

```- #### Links with Different TonesDescriptionDemonstrates how links can have different visual tones, including default, neutral, and critical, allowing for varied contextual styling.jsx```

<s-stack gap="base">

<s-paragraph>

Default tone: <s-link>View orders</s-link>

</s-paragraph>

<s-paragraph tone="success">

Success tone: <s-link>Inventory help</s-link>

</s-paragraph>

<s-paragraph tone="critical">

Critical tone: <s-link>Close store</s-link>

</s-paragraph>

<s-paragraph tone="warning">

Warning tone: <s-link>Update billing info</s-link>

</s-paragraph>

<s-paragraph tone="info">

Info tone: <s-link>Learn more about reports</s-link>

</s-paragraph>

<s-paragraph tone="caution">

Caution tone: <s-link>View archived products</s-link>

</s-paragraph>

</s-stack>

```html```

<s-stack gap="base">

<s-paragraph>

Default tone: <s-link>View orders</s-link>

</s-paragraph>

<s-paragraph tone="success">

Neutral tone: <s-link>Inventory help</s-link>

</s-paragraph>

<s-paragraph tone="critical">

Critical tone: <s-link>Close store</s-link>

</s-paragraph>

<s-paragraph tone="warning">

Warning tone: <s-link>Update billing info</s-link>

</s-paragraph>

<s-paragraph tone="info">

Info tone: <s-link>Learn more about reports</s-link>

</s-paragraph>

<s-paragraph tone="caution">

Subdued tone: <s-link>View archived products</s-link>

</s-paragraph>

</s-stack>

```## [Anchor to best-practices](/docs/api/admin-extensions/latest/polaris-web-components/actions/link#best-practices)Best practices

- Use links for navigation and buttons for actions

- Use default links whenever possible to avoid disorienting merchants

- Open external links in a new tab only when merchants are performing a task or navigating outside the Shopify admin

Was this page helpful?YesNo### Updates- [Developer changelog](/changelog)- [Shopify Editions](https://www.shopify.com/editions)### Business growth- [Shopify Partners Program](https://www.shopify.com/partners?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Shopify App Store](https://apps.shopify.com/?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Shopify Academy](https://www.shopifyacademy.com/page/catalog#role_developer?utm_source=web_dotdev&utm_medium=footer_businessgrowth)### Legal- [Terms of service](https://www.shopify.com/legal/terms?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [API terms of use](https://www.shopify.com/legal/api-terms?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Privacy policy](https://www.shopify.com/legal/privacy?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Partners Program Agreement](https://www.shopify.com/partners/terms?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)### Shopify- [About Shopify](https://www.shopify.com/about?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Shopify Plus](https://www.shopify.com/plus?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Careers](https://www.shopify.com/careers?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Investors](https://investors.shopify.com/home/default.aspx?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Press and media](https://shopify.com/news?shpxid=7db0d4e4-24E8-4087-58FA-7EE470CA745A)