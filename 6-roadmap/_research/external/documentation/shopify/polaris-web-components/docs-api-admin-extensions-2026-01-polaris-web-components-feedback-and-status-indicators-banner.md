---
{
  "fetch": {
    "url": "https://shopify.dev/docs/api/admin-extensions/2026-01/polaris-web-components/feedback-and-status-indicators/banner",
    "fetched_at": "2026-02-10T13:29:33.649397",
    "status": 200,
    "size_bytes": 281488
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

Choose a version:2026-01 latest2025-10 2025-07 2025-04 2025-01 2024-10 2024-07 2024-04 2024-01 2023-10 2026-01latest# BannerAsk assistantHighlights important information or required actions prominently within the interface. Use to communicate statuses, provide feedback, or draw attention to critical updates.

## [Anchor to properties](/docs/api/admin-extensions/latest/polaris-web-components/feedback-and-status-indicators/banner#properties)Properties[Anchor to dismissible](/docs/api/admin-extensions/latest/polaris-web-components/feedback-and-status-indicators/banner#properties-propertydetail-dismissible)dismissible**dismissible**boolean**boolean**Default: false**Default: false**Determines whether the close button of the banner is present.

When the close button is pressed, the `dismiss` event will fire, then `hidden` will be true, any animation will complete, and the `afterhide` event will fire.

[Anchor to heading](/docs/api/admin-extensions/latest/polaris-web-components/feedback-and-status-indicators/banner#properties-propertydetail-heading)heading**heading**string**string**Default: ''**Default: ''**The title of the banner.

[Anchor to hidden](/docs/api/admin-extensions/latest/polaris-web-components/feedback-and-status-indicators/banner#properties-propertydetail-hidden)hidden**hidden**boolean**boolean**Default: false**Default: false**Determines whether the banner is hidden.

If this property is being set on each framework render (as in 'controlled' usage), and the banner is `dismissible`, ensure you update app state for this property when the `dismiss` event fires.

If the banner is not `dismissible`, it can still be hidden by setting this property.

[Anchor to tone](/docs/api/admin-extensions/latest/polaris-web-components/feedback-and-status-indicators/banner#properties-propertydetail-tone)tone**tone**"info" | "success" | "warning" | "critical" | "auto"**"info" | "success" | "warning" | "critical" | "auto"**Default: 'auto'**Default: 'auto'**Sets the tone of the Banner, based on the intention of the information being conveyed.

The banner is a live region and the type of status will be dictated by the Tone selected.

- `critical` creates an [assertive live region](https://developer.mozilla.org/en-US/docs/Web/Accessibility/ARIA/Roles/alert_role) that is announced by screen readers immediately.

- `neutral`, `info`, `success`, `warning` and `caution` creates an [informative live region](https://developer.mozilla.org/en-US/docs/Web/Accessibility/ARIA/Roles/status_role) that is announced by screen readers after the current message.

## [Anchor to events](/docs/api/admin-extensions/latest/polaris-web-components/feedback-and-status-indicators/banner#events)EventsLearn more about [registering events](/docs/api/app-home/using-polaris-components#event-handling).

[Anchor to afterhide](/docs/api/admin-extensions/latest/polaris-web-components/feedback-and-status-indicators/banner#events-propertydetail-afterhide)afterhide**afterhide**CallbackEventListenerCallbackEventListener<typeof tagName> | null**CallbackEventListenerCallbackEventListener<typeof tagName> | null**[Anchor to dismiss](/docs/api/admin-extensions/latest/polaris-web-components/feedback-and-status-indicators/banner#events-propertydetail-dismiss)dismiss**dismiss**CallbackEventListenerCallbackEventListener<typeof tagName> | null**CallbackEventListenerCallbackEventListener<typeof tagName> | null**### CallbackEventListener```

(EventListener & {

(event: CallbackEvent<T>): void;

}) | null

```### CallbackEvent```

Event & {

currentTarget: HTMLElementTagNameMap[T];

}

```## [Anchor to slots](/docs/api/admin-extensions/latest/polaris-web-components/feedback-and-status-indicators/banner#slots)Slots[Anchor to children](/docs/api/admin-extensions/latest/polaris-web-components/feedback-and-status-indicators/banner#slots-propertydetail-children)children**children**HTMLElement**HTMLElement**The content of the Banner.

[Anchor to secondary-actions](/docs/api/admin-extensions/latest/polaris-web-components/feedback-and-status-indicators/banner#slots-propertydetail-secondaryactions)secondary-actions**secondary-actions**HTMLElement**HTMLElement**The secondary actions to display at the bottom of the Banner.

Only Buttons with the `variant` of "secondary" or "auto" are permitted. A maximum of two `s-button` components are allowed.

ExamplesCodejsxhtmlCopy9123<s-banner heading="Order archived" tone="info" dismissible>  This order was archived on March 7, 2017 at 3:12pm EDT.</s-banner>## Preview### Examples- #### Codejsx```

<s-banner heading="Order archived" tone="info" dismissible>

This order was archived on March 7, 2017 at 3:12pm EDT.

</s-banner>

```html```

<s-banner heading="Order archived" tone="info" dismissible>

This order was archived on March 7, 2017 at 3:12pm EDT.

</s-banner>

```- #### Basic information bannerDescriptionDemonstrates a simple informational banner used to communicate status updates or completed actions, providing clear and concise feedback to the user.jsx```

<s-banner heading="Order archived">

This order was archived on March 7, 2017 at 3:12pm EDT.

</s-banner>

```html```

<s-banner heading="Order archived">

This order was archived on March 7, 2017 at 3:12pm EDT.

</s-banner>

```- #### Warning banner with specific actionsDescriptionIllustrates a warning banner that highlights a potential issue and provides actionable buttons to help users resolve the problem quickly and effectively.jsx```

<s-banner heading="127 products missing shipping weights" tone="warning">

Products without weights may show inaccurate shipping rates, leading to

checkout abandonment.

<s-button

slot="secondary-actions"

variant="secondary"

href="/admin/products?filter=missing-weights"

>

Review products

</s-button>

<s-button

slot="secondary-actions"

variant="secondary"

href="javascript:void(0)"

>

Setup guide

</s-button>

</s-banner>

```html```

<s-banner heading="127 products missing shipping weights" tone="warning">

Products without weights may show inaccurate shipping rates, leading to

checkout abandonment.

<s-button

slot="secondary-actions"

variant="secondary"

href="/admin/products?filter=missing-weights"

>

Review products

</s-button>

<s-button

slot="secondary-actions"

variant="secondary"

href="javascript:void(0)"

>

Setup guide

</s-button>

</s-banner>

```- #### Critical banner with clear next stepsDescriptionDemonstrates an urgent banner design that signals a critical issue requiring immediate action, with clear and prominent secondary action buttons to guide users.jsx```

<s-banner heading="Order #1024 flagged for fraud review" tone="critical">

This order shows multiple risk indicators and cannot be auto-fulfilled. Review

required within 24 hours to prevent automatic cancellation.

<s-button

slot="secondary-actions"

variant="secondary"

href="/admin/orders/1024/risk"

>

Review order details

</s-button>

<s-button

slot="secondary-actions"

variant="secondary"

href="/admin/settings/payments/fraud"

>

Adjust fraud settings

</s-button>

</s-banner>

```html```

<s-banner heading="Order #1024 flagged for fraud review" tone="critical">

This order shows multiple risk indicators and cannot be auto-fulfilled. Review

required within 24 hours to prevent automatic cancellation.

<s-button

slot="secondary-actions"

variant="secondary"

href="/admin/orders/1024/risk"

>

Review order details

</s-button>

<s-button

slot="secondary-actions"

variant="secondary"

href="/admin/settings/payments/fraud"

>

Adjust fraud settings

</s-button>

</s-banner>

```- #### Dismissible success bannerDescriptionSuccess confirmation with dismiss option for completed operations.jsx```

<s-banner heading="Products imported" tone="success" dismissible={true}>

Successfully imported 50 products to your store.

</s-banner>

```html```

<s-banner heading="Products imported" tone="success" dismissible="true">

Successfully imported 50 products to your store.

</s-banner>

```- #### Info banner with clear value propositionDescriptionInformational banner highlighting app updates with clear benefits and actions.jsx```

<s-banner heading="Point of Sale v2.4 available" tone="info" dismissible>

New version includes faster checkout processing and inventory sync

improvements.

<s-button

slot="secondary-actions"

variant="secondary"

href="/admin/apps/pos/changelog"

>

View changes

</s-button>

<s-button slot="secondary-actions" variant="secondary">

Install update

</s-button>

</s-banner>

```html```

<s-banner heading="Point of Sale v2.4 available" tone="info" dismissible>

New version includes faster checkout processing and inventory sync

improvements.

<s-button

slot="secondary-actions"

variant="secondary"

href="/admin/apps/pos/changelog"

>

View changes

</s-button>

<s-button slot="secondary-actions" variant="secondary">

Install update

</s-button>

</s-banner>

```## [Anchor to useful-for](/docs/api/admin-extensions/latest/polaris-web-components/feedback-and-status-indicators/banner#useful-for)Useful for

- Showing important information or changes

- Prompting merchants to take a specific action

- Displaying warnings, errors, or critical information

- Communicating persistent conditions that need attention

## [Anchor to outside-of-a-section](/docs/api/admin-extensions/latest/polaris-web-components/feedback-and-status-indicators/banner#outside-of-a-section)Outside of a sectionBanners placed outside of a section will display in their own card and should be located at the top of the page. They're useful for conveying messages that apply to the entire page or areas not visible within the viewport, such as validation errors further down the page.

## [Anchor to in-a-section](/docs/api/admin-extensions/latest/polaris-web-components/feedback-and-status-indicators/banner#in-a-section)In a sectionBanners placed inside a section will have styles applied contextually. They're useful for conveying messages relevant to a specific section or piece of content.

## [Anchor to best-practices](/docs/api/admin-extensions/latest/polaris-web-components/feedback-and-status-indicators/banner#best-practices)Best practices

- Seeing these banners can be stressful, so use them sparingly to avoid overwhelming users.

- Focus on a single piece of information or required action to avoid overwhelming users.

- Make the message concise and scannable. Users shouldn’t need to spend a lot of time figuring out what they need to know and do.

- Info, Warning and Critical banners should contain a call to action and clear next steps. Users should know what to do after seeing the banner.

- Avoid banners that can't be dismissed unless the user is required to take action.

## [Anchor to content-guidelines](/docs/api/admin-extensions/latest/polaris-web-components/feedback-and-status-indicators/banner#content-guidelines)Content guidelines

- Keep titles concise and clear

- Limit body content to 1-2 sentences where possible

- Use action-led buttons with strong verbs (e.g., "Activate Apple Pay" not "Try Apple Pay")

- Avoid unnecessary words and articles in button text

- For warning and critical banners, explain how to resolve the issue

Was this page helpful?YesNo### Updates- [Developer changelog](/changelog)- [Shopify Editions](https://www.shopify.com/editions)### Business growth- [Shopify Partners Program](https://www.shopify.com/partners?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Shopify App Store](https://apps.shopify.com/?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Shopify Academy](https://www.shopifyacademy.com/page/catalog#role_developer?utm_source=web_dotdev&utm_medium=footer_businessgrowth)### Legal- [Terms of service](https://www.shopify.com/legal/terms?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [API terms of use](https://www.shopify.com/legal/api-terms?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Privacy policy](https://www.shopify.com/legal/privacy?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Partners Program Agreement](https://www.shopify.com/partners/terms?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)### Shopify- [About Shopify](https://www.shopify.com/about?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Shopify Plus](https://www.shopify.com/plus?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Careers](https://www.shopify.com/careers?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Investors](https://investors.shopify.com/home/default.aspx?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Press and media](https://shopify.com/news?shpxid=7db0d4e4-24E8-4087-58FA-7EE470CA745A)