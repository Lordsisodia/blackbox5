---
{
  "fetch": {
    "url": "https://shopify.dev/docs/api/admin-extensions/2026-01/polaris-web-components/layout-and-structure/querycontainer",
    "fetched_at": "2026-02-10T13:30:32.757294",
    "status": 200,
    "size_bytes": 252685
  },
  "metadata": {
    "title": "QueryContainer",
    "source": "shopify",
    "category": "polaris-web-components",
    "section": "layout-and-structure",
    "component": "querycontainer"
  }
}
---

# QueryContainer

Choose a version:2026-01 latest2025-10 2025-07 2025-04 2025-01 2024-10 2024-07 2024-04 2024-01 2023-10 2026-01latest# QueryContainerAsk assistantEstablishes a query container for responsive design. Use `s-query-container` to define an element as a containment context, enabling child components or styles to adapt based on the container’s size.

## [Anchor to properties](/docs/api/admin-extensions/latest/polaris-web-components/layout-and-structure/querycontainer#properties)PropertiesUse to define an element as a containment context, enabling child components or styles to adapt based on the container’s size.

[Anchor to containerName](/docs/api/admin-extensions/latest/polaris-web-components/layout-and-structure/querycontainer#properties-propertydetail-containername)containerName**containerName**string**string**Default: ''**Default: ''**The name of the container, which can be used in your container queries to target this container specifically.

We place the container name of `s-default` on every container. Because of this, it is not required to add a `containerName` identifier in your queries. For example, a `@container (inline-size <= 300px) none, auto` query is equivalent to `@container s-default (inline-size <= 300px) none, auto`.

Any value set in `containerName` will be set alongside alongside `s-default`. For example, `containerName="my-container-name"` will result in a value of `s-default my-container-name` set on the `container-name` CSS property of the rendered HTML.

## [Anchor to slots](/docs/api/admin-extensions/latest/polaris-web-components/layout-and-structure/querycontainer#slots)Slots[Anchor to children](/docs/api/admin-extensions/latest/polaris-web-components/layout-and-structure/querycontainer#slots-propertydetail-children)children**children**HTMLElement**HTMLElement**The content of the container.

ExamplesExamplejsxhtmlCopy912345678<s-query-container>  <s-box    padding="@container (inline-size > 500px) large-500, none"    background="strong"  >    Padding is applied when the inline-size > 500px  </s-box></s-query-container>## Preview### Examples- #### jsx```

<s-query-container>

<s-box

padding="@container (inline-size > 500px) large-500, none"

background="strong"

>

Padding is applied when the inline-size > 500px

</s-box>

</s-query-container>

```html```

<s-query-container>

<s-box

padding="@container (inline-size > 500px) large-500, none"

background="strong"

>

Padding is applied when the inline-size '>' 500px

</s-box>

</s-query-container>

```- #### Basic UsageDescriptionDemonstrates the simplest way to use QueryContainer, wrapping content with a named container context.jsx```

<>

<s-box inlineSize="375px">

<s-query-container id="product-section" containerName="product">

<s-box padding="@container product (inline-size > 400px) large-500, none" borderWidth="base" borderColor="base" borderRadius="base">

<s-text>Padding is different depending on the container size</s-text>

</s-box>

</s-query-container>

</s-box>

<s-box inlineSize="450px">

<s-query-container id="product-section" containerName="product">

<s-box padding="@container product (inline-size > 400px) large-500, none" borderWidth="base" borderColor="base" borderRadius="base">

<s-text>Padding is different depending on the container size</s-text>

</s-box>

</s-query-container>

</s-box>

</>

```html```

<s-box inlineSize="375px">

<s-query-container id="product-section" containerName="product">

<s-box padding="@container product (inline-size > 400px) large-500, none">

<s-text>Padding is different depending on the container size</s-text>

</s-box>

</s-query-container>

</s-box>

<s-box inlineSize="450px">

<s-query-container id="product-section" containerName="product">

<s-box padding="@container product (inline-size > 400px) large-500, none">

<s-text>Padding is different depending on the container size</s-text>

</s-box>

</s-query-container>

</s-box>

```Was this page helpful?YesNo### Updates- [Developer changelog](/changelog)- [Shopify Editions](https://www.shopify.com/editions)### Business growth- [Shopify Partners Program](https://www.shopify.com/partners?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Shopify App Store](https://apps.shopify.com/?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Shopify Academy](https://www.shopifyacademy.com/page/catalog#role_developer?utm_source=web_dotdev&utm_medium=footer_businessgrowth)### Legal- [Terms of service](https://www.shopify.com/legal/terms?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [API terms of use](https://www.shopify.com/legal/api-terms?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Privacy policy](https://www.shopify.com/legal/privacy?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Partners Program Agreement](https://www.shopify.com/partners/terms?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)### Shopify- [About Shopify](https://www.shopify.com/about?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Shopify Plus](https://www.shopify.com/plus?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Careers](https://www.shopify.com/careers?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Investors](https://investors.shopify.com/home/default.aspx?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Press and media](https://shopify.com/news?shpxid=7db0d4e4-24E8-4087-58FA-7EE470CA745A)