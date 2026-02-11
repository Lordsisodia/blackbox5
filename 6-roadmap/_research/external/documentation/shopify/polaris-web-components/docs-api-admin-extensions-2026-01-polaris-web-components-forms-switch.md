---
{
  "fetch": {
    "url": "https://shopify.dev/docs/api/admin-extensions/2026-01/polaris-web-components/forms/switch",
    "fetched_at": "2026-02-10T13:30:07.757030",
    "status": 200,
    "size_bytes": 281649
  },
  "metadata": {
    "title": "Switch",
    "source": "shopify",
    "category": "polaris-web-components",
    "section": "forms",
    "component": "switch"
  }
}
---

# Switch

Choose a version:2026-01 latest2025-10 2025-07 2025-04 2025-01 2024-10 2024-07 2024-04 2024-01 2023-10 2026-01latest# SwitchAsk assistantGive users a clear way to toggle options on or off.

## [Anchor to properties](/docs/api/admin-extensions/latest/polaris-web-components/forms/switch#properties)Properties[Anchor to accessibilityLabel](/docs/api/admin-extensions/latest/polaris-web-components/forms/switch#properties-propertydetail-accessibilitylabel)accessibilityLabel**accessibilityLabel**string**string**A label used for users using assistive technologies like screen readers. When set, any children or `label` supplied will not be announced. This can also be used to display a control without a visual label, while still providing context to users using screen readers.

[Anchor to checked](/docs/api/admin-extensions/latest/polaris-web-components/forms/switch#properties-propertydetail-checked)checked**checked**boolean**boolean**Default: false**Default: false**Whether the control is active.

[Anchor to defaultChecked](/docs/api/admin-extensions/latest/polaris-web-components/forms/switch#properties-propertydetail-defaultchecked)defaultChecked**defaultChecked**boolean**boolean**Default: false**Default: false**Whether the control is active by default.

[Anchor to details](/docs/api/admin-extensions/latest/polaris-web-components/forms/switch#properties-propertydetail-details)details**details**string**string**Additional text to provide context or guidance for the field. This text is displayed along with the field and its label to offer more information or instructions to the user.

This will also be exposed to screen reader users.

[Anchor to disabled](/docs/api/admin-extensions/latest/polaris-web-components/forms/switch#properties-propertydetail-disabled)disabled**disabled**boolean**boolean**Default: false**Default: false**Disables the field, disallowing any interaction.

[Anchor to error](/docs/api/admin-extensions/latest/polaris-web-components/forms/switch#properties-propertydetail-error)error**error**string**string**Indicate an error to the user. The field will be given a specific stylistic treatment to communicate problems that have to be resolved immediately.

[Anchor to id](/docs/api/admin-extensions/latest/polaris-web-components/forms/switch#properties-propertydetail-id)id**id**string**string**A unique identifier for the element.

[Anchor to label](/docs/api/admin-extensions/latest/polaris-web-components/forms/switch#properties-propertydetail-label)label**label**string**string**Visual content to use as the control label.

[Anchor to labelAccessibilityVisibility](/docs/api/admin-extensions/latest/polaris-web-components/forms/switch#properties-propertydetail-labelaccessibilityvisibility)labelAccessibilityVisibility**labelAccessibilityVisibility**"visible" | "exclusive"**"visible" | "exclusive"**Default: 'visible'**Default: 'visible'**Changes the visibility of the component's label.

- `visible`: the label is visible to all users.

- `exclusive`: the label is visually hidden but remains in the accessibility tree.

[Anchor to name](/docs/api/admin-extensions/latest/polaris-web-components/forms/switch#properties-propertydetail-name)name**name**string**string**An identifier for the field that is unique within the nearest containing form.

[Anchor to required](/docs/api/admin-extensions/latest/polaris-web-components/forms/switch#properties-propertydetail-required)required**required**boolean**boolean**Default: false**Default: false**Whether the field needs a value. This requirement adds semantic value to the field, but it will not cause an error to appear automatically. If you want to present an error when this field is empty, you can do so with the `error` property.

[Anchor to value](/docs/api/admin-extensions/latest/polaris-web-components/forms/switch#properties-propertydetail-value)value**value**string**string**The value used in form data when the checkbox is checked.

## [Anchor to events](/docs/api/admin-extensions/latest/polaris-web-components/forms/switch#events)EventsLearn more about [registering events](/docs/api/app-home/using-polaris-components#event-handling).

[Anchor to change](/docs/api/admin-extensions/latest/polaris-web-components/forms/switch#events-propertydetail-change)change**change**CallbackEventListenerCallbackEventListener<'input'>**CallbackEventListenerCallbackEventListener<'input'>**[Anchor to input](/docs/api/admin-extensions/latest/polaris-web-components/forms/switch#events-propertydetail-input)input**input**CallbackEventListenerCallbackEventListener<'input'>**CallbackEventListenerCallbackEventListener<'input'>**### CallbackEventListener```

(EventListener & {

(event: CallbackEvent<T>): void;

}) | null

```### CallbackEvent```

Event & {

currentTarget: HTMLElementTagNameMap[T];

}

```ExamplesCodejsxhtmlCopy91234<s-switch  label="Enable feature"  details="Ensure all criteria are met before enabling" />## Preview### Examples- #### Codejsx```

<s-switch

label="Enable feature"

details="Ensure all criteria are met before enabling"

/>

```html```

<s-switch

label="Enable feature"

details="Ensure all criteria are met before enabling"

></s-switch>

```- #### Basic switchDescriptionStandard toggle switch for enabling or disabling merchant preferences. This example demonstrates a simple switch with a label, allowing users to toggle a single setting on or off.jsx```

<s-switch id="basic-switch" label="Enable notifications" />

```html```

<s-switch id="basic-switch" label="Enable notifications"></s-switch>

```- #### Disabled switchDescriptionLocked switch with explanatory text for unavailable premium features. This example shows a switch that is visually disabled and cannot be interacted with, typically used to indicate a feature is not currently available.jsx```

<s-switch

id="disabled-switch"

label="Feature locked (Premium plan required)"

checked={true}

disabled={true}

/>

```html```

<s-switch

id="disabled-switch"

label="Feature locked (Premium plan required)"

checked="true"

disabled="true"

></s-switch>

```- #### Form integrationDescriptionMultiple switches within a form for notification preferences submission. This example illustrates how switches can be used together in a form to allow users to configure multiple related settings simultaneously.jsx```

<form>

<s-switch

id="email-notifications"

label="Email notifications"

name="emailNotifications"

value="enabled"

/>

<s-switch

id="sms-notifications"

label="SMS notifications"

name="smsNotifications"

value="enabled"

/>

</form>

```html```

<form>

<s-switch

id="email-notifications"

label="Email notifications"

name="emailNotifications"

value="enabled"

></s-switch>

<s-switch

id="sms-notifications"

label="SMS notifications"

name="smsNotifications"

value="enabled"

></s-switch>

</form>

```- #### Hidden label for accessibilityDescriptionSwitch with visually hidden label that remains accessible to screen readers. This example demonstrates how to create a switch with a label that is only perceivable by assistive technologies, maintaining accessibility while minimizing visual clutter.jsx```

<s-switch

id="hidden-label-switch"

labelAccessibilityVisibility="exclusive"

label="Toggle feature"

checked={true}

/>

```html```

<s-switch

id="hidden-label-switch"

labelAccessibilityVisibility="exclusive"

label="Toggle feature"

checked="true"

></s-switch>

```- #### With details and errorDescriptionRequired switch with validation error and contextual details for user guidance. This example shows a switch that requires user interaction, provides additional context through details, and displays an error message when validation fails.jsx```

<s-switch

id="terms-switch"

label="Agree to terms and conditions"

details="You must agree to continue with the purchase"

error="Agreement is required"

name="termsAgreement"

required={true}

value="agreed"

/>

```html```

<s-switch

id="terms-switch"

label="Agree to terms and conditions"

details="You must agree to continue with the purchase"

error="Agreement is required"

name="termsAgreement"

required="true"

value="agreed"

></s-switch>

```- #### Switch with accessibility labelDescriptionSwitch with enhanced accessibility description for screen reader users. This example illustrates how to provide a more descriptive accessibility label that provides additional context beyond the visible label.jsx```

<s-switch

id="event-switch"

label="Feature toggle"

accessibilityLabel="Toggle feature on or off"

/>

```html```

<s-switch

id="event-switch"

label="Feature toggle"

accessibilityLabel="Toggle feature on or off"

></s-switch>

```- #### Settings panel with StackDescriptionGroup of related switches arranged in a vertical stack for settings configuration. This example demonstrates how to use the Stack component to create a clean, organized layout for multiple related switch settings.jsx```

<s-stack gap="small-200">

<s-switch id="notifications-setting" label="Push notifications" />

<s-switch id="autosave-setting" label="Auto-save drafts" />

<s-switch

id="analytics-setting"

label="Usage analytics"

checked={true}

/>

</s-stack>

```html```

<s-stack gap="base">

<s-switch id="notifications-setting" label="Push notifications"></s-switch>

<s-switch id="autosave-setting" label="Auto-save drafts"></s-switch>

<s-switch

id="analytics-setting"

label="Usage analytics"

checked="true"

></s-switch>

</s-stack>

```Was this page helpful?YesNo### Updates- [Developer changelog](/changelog)- [Shopify Editions](https://www.shopify.com/editions)### Business growth- [Shopify Partners Program](https://www.shopify.com/partners?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Shopify App Store](https://apps.shopify.com/?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Shopify Academy](https://www.shopifyacademy.com/page/catalog#role_developer?utm_source=web_dotdev&utm_medium=footer_businessgrowth)### Legal- [Terms of service](https://www.shopify.com/legal/terms?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [API terms of use](https://www.shopify.com/legal/api-terms?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Privacy policy](https://www.shopify.com/legal/privacy?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Partners Program Agreement](https://www.shopify.com/partners/terms?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)### Shopify- [About Shopify](https://www.shopify.com/about?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Shopify Plus](https://www.shopify.com/plus?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Careers](https://www.shopify.com/careers?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Investors](https://investors.shopify.com/home/default.aspx?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Press and media](https://shopify.com/news?shpxid=7db0d4e4-24E8-4087-58FA-7EE470CA745A)