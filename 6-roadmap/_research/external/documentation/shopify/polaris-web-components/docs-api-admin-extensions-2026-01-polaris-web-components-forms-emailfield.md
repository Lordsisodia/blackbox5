---
{
  "fetch": {
    "url": "https://shopify.dev/docs/api/admin-extensions/2026-01/polaris-web-components/forms/emailfield",
    "fetched_at": "2026-02-10T13:29:51.488494",
    "status": 200,
    "size_bytes": 296142
  },
  "metadata": {
    "title": "EmailField",
    "source": "shopify",
    "category": "polaris-web-components",
    "section": "forms",
    "component": "emailfield"
  }
}
---

# EmailField

Choose a version:2026-01 latest2025-10 2025-07 2025-04 2025-01 2024-10 2024-07 2024-04 2024-01 2023-10 2026-01latest# EmailFieldAsk assistantLet users enter email addresses with optimized keyboard settings.

## [Anchor to properties](/docs/api/admin-extensions/latest/polaris-web-components/forms/emailfield#properties)Properties[Anchor to autocomplete](/docs/api/admin-extensions/latest/polaris-web-components/forms/emailfield#properties-propertydetail-autocomplete)autocomplete**autocomplete**"on" | "off" | EmailAutocompleteFieldEmailAutocompleteField | `section-${string} email` | `section-${string} home email` | `section-${string} mobile email` | `section-${string} fax email` | `section-${string} pager email` | "shipping email" | "shipping home email" | "shipping mobile email" | "shipping fax email" | "shipping pager email" | "billing email" | "billing home email" | "billing mobile email" | "billing fax email" | "billing pager email" | `section-${string} shipping email` | `section-${string} shipping home email` | `section-${string} shipping mobile email` | `section-${string} shipping fax email` | `section-${string} shipping pager email` | `section-${string} billing email` | `section-${string} billing home email` | `section-${string} billing mobile email` | `section-${string} billing fax email` | `section-${string} billing pager email`**"on" | "off" | EmailAutocompleteFieldEmailAutocompleteField | `section-${string} email` | `section-${string} home email` | `section-${string} mobile email` | `section-${string} fax email` | `section-${string} pager email` | "shipping email" | "shipping home email" | "shipping mobile email" | "shipping fax email" | "shipping pager email" | "billing email" | "billing home email" | "billing mobile email" | "billing fax email" | "billing pager email" | `section-${string} shipping email` | `section-${string} shipping home email` | `section-${string} shipping mobile email` | `section-${string} shipping fax email` | `section-${string} shipping pager email` | `section-${string} billing email` | `section-${string} billing home email` | `section-${string} billing mobile email` | `section-${string} billing fax email` | `section-${string} billing pager email`**Default: 'on' for everything else**Default: 'on' for everything else**A hint as to the intended content of the field.

When set to `on` (the default), this property indicates that the field should support autofill, but you do not have any more semantic information on the intended contents.

When set to `off`, you are indicating that this field contains sensitive information, or contents that are never saved, like one-time codes.

Alternatively, you can provide value which describes the specific data you would like to be entered into this field during autofill.

[Anchor to defaultValue](/docs/api/admin-extensions/latest/polaris-web-components/forms/emailfield#properties-propertydetail-defaultvalue)defaultValue**defaultValue**string**string**The default value for the field.

[Anchor to details](/docs/api/admin-extensions/latest/polaris-web-components/forms/emailfield#properties-propertydetail-details)details**details**string**string**Additional text to provide context or guidance for the field. This text is displayed along with the field and its label to offer more information or instructions to the user.

This will also be exposed to screen reader users.

[Anchor to disabled](/docs/api/admin-extensions/latest/polaris-web-components/forms/emailfield#properties-propertydetail-disabled)disabled**disabled**boolean**boolean**Default: false**Default: false**Disables the field, disallowing any interaction.

[Anchor to error](/docs/api/admin-extensions/latest/polaris-web-components/forms/emailfield#properties-propertydetail-error)error**error**string**string**Indicate an error to the user. The field will be given a specific stylistic treatment to communicate problems that have to be resolved immediately.

[Anchor to id](/docs/api/admin-extensions/latest/polaris-web-components/forms/emailfield#properties-propertydetail-id)id**id**string**string**A unique identifier for the element.

[Anchor to label](/docs/api/admin-extensions/latest/polaris-web-components/forms/emailfield#properties-propertydetail-label)label**label**string**string**Content to use as the field label.

[Anchor to labelAccessibilityVisibility](/docs/api/admin-extensions/latest/polaris-web-components/forms/emailfield#properties-propertydetail-labelaccessibilityvisibility)labelAccessibilityVisibility**labelAccessibilityVisibility**"visible" | "exclusive"**"visible" | "exclusive"**Default: 'visible'**Default: 'visible'**Changes the visibility of the component's label.

- `visible`: the label is visible to all users.

- `exclusive`: the label is visually hidden but remains in the accessibility tree.

[Anchor to maxLength](/docs/api/admin-extensions/latest/polaris-web-components/forms/emailfield#properties-propertydetail-maxlength)maxLength**maxLength**number**number**Default: Infinity**Default: Infinity**Specifies the maximum number of characters allowed.

[Anchor to minLength](/docs/api/admin-extensions/latest/polaris-web-components/forms/emailfield#properties-propertydetail-minlength)minLength**minLength**number**number**Default: 0**Default: 0**Specifies the min number of characters allowed.

[Anchor to name](/docs/api/admin-extensions/latest/polaris-web-components/forms/emailfield#properties-propertydetail-name)name**name**string**string**An identifier for the field that is unique within the nearest containing form.

[Anchor to placeholder](/docs/api/admin-extensions/latest/polaris-web-components/forms/emailfield#properties-propertydetail-placeholder)placeholder**placeholder**string**string**A short hint that describes the expected value of the field.

[Anchor to readOnly](/docs/api/admin-extensions/latest/polaris-web-components/forms/emailfield#properties-propertydetail-readonly)readOnly**readOnly**boolean**boolean**Default: false**Default: false**The field cannot be edited by the user. It is focusable will be announced by screen readers.

[Anchor to required](/docs/api/admin-extensions/latest/polaris-web-components/forms/emailfield#properties-propertydetail-required)required**required**boolean**boolean**Default: false**Default: false**Whether the field needs a value. This requirement adds semantic value to the field, but it will not cause an error to appear automatically. If you want to present an error when this field is empty, you can do so with the `error` property.

[Anchor to value](/docs/api/admin-extensions/latest/polaris-web-components/forms/emailfield#properties-propertydetail-value)value**value**string**string**The current value for the field. If omitted, the field will be empty.

### EmailAutocompleteField```

'email' | 'home email' | 'mobile email' | 'fax email' | 'pager email'

```## [Anchor to events](/docs/api/admin-extensions/latest/polaris-web-components/forms/emailfield#events)EventsLearn more about [registering events](/docs/api/app-home/using-polaris-components#event-handling).

[Anchor to blur](/docs/api/admin-extensions/latest/polaris-web-components/forms/emailfield#events-propertydetail-blur)blur**blur**CallbackEventListenerCallbackEventListener<'input'>**CallbackEventListenerCallbackEventListener<'input'>**[Anchor to change](/docs/api/admin-extensions/latest/polaris-web-components/forms/emailfield#events-propertydetail-change)change**change**CallbackEventListenerCallbackEventListener<'input'>**CallbackEventListenerCallbackEventListener<'input'>**[Anchor to focus](/docs/api/admin-extensions/latest/polaris-web-components/forms/emailfield#events-propertydetail-focus)focus**focus**CallbackEventListenerCallbackEventListener<'input'>**CallbackEventListenerCallbackEventListener<'input'>**[Anchor to input](/docs/api/admin-extensions/latest/polaris-web-components/forms/emailfield#events-propertydetail-input)input**input**CallbackEventListenerCallbackEventListener<'input'>**CallbackEventListenerCallbackEventListener<'input'>**### CallbackEventListener```

(EventListener & {

(event: CallbackEvent<T>): void;

}) | null

```### CallbackEvent```

Event & {

currentTarget: HTMLElementTagNameMap[T];

}

```ExamplesCodejsxhtmlCopy912345<s-email-field  label="Email"  placeholder="bernadette.lapresse@jadedpixel.com"  details="Used for sending notifications" />## Preview### Examples- #### Codejsx```

<s-email-field

label="Email"

placeholder="bernadette.lapresse@jadedpixel.com"

details="Used for sending notifications"

/>

```html```

<s-email-field

label="Email"

placeholder="bernadette.lapresse@jadedpixel.com"

details="Used for sending notifications"

></s-email-field>

```- #### Basic usageDescriptionDemonstrates a simple email field with a label and required attribute, showing the most fundamental way to use the EmailField component.jsx```

<s-stack gap="base">

<s-email-field label="Email address" required />

</s-stack>

```html```

<s-stack gap="base">

<s-email-field label="Email address" required></s-email-field>

</s-stack>

```- #### With error and help textDescriptionShowcases an email field with additional details and an error message, illustrating how to provide contextual information and validation feedback.jsx```

<s-stack gap="base">

<s-email-field

label="Contact email"

details="We'll send your order confirmation here"

error="Please enter a valid email address"

required

/>

</s-stack>

```html```

<s-stack gap="base">

<s-email-field

label="Contact email"

details="We'll send your order confirmation here"

error="Please enter a valid email address"

required

></s-email-field>

</s-stack>

```- #### Optional field with placeholderDescriptionIllustrates an optional email field with a placeholder text and help text, demonstrating a common pattern for collecting alternative contact information.jsx```

<s-stack gap="base">

<s-email-field

label="Alternate email"

placeholder="secondary@example.com"

details="Additional email for notifications"

/>

</s-stack>

```html```

<s-stack gap="base">

<s-email-field

label="Alternate email"

placeholder="secondary@example.com"

details="Additional email for notifications"

></s-email-field>

</s-stack>

```- #### Read-only displayDescriptionShows how to render an email field in a read-only state, useful for displaying existing email addresses that cannot be modified.jsx```

<s-stack gap="base">

<s-email-field

label="Account email"

value="user@example.com"

readOnly

/>

</s-stack>

```html```

<s-stack gap="base">

<s-email-field

label="Account email"

value="user@example.com"

readOnly

></s-email-field>

</s-stack>

```- #### With length constraintsDescriptionDemonstrates setting minimum and maximum length constraints for the email input, providing additional validation beyond the standard email format check.jsx```

<s-stack gap="base">

<s-email-field

label="Business email"

minLength={5}

maxLength={100}

required

/>

</s-stack>

```html```

<s-stack gap="base">

<s-email-field

label="Business email"

minLength="5"

maxLength="100"

required

></s-email-field>

</s-stack>

```- #### Email validationDescriptionInteractive example showing real-time email validation with error messages that update as the user types.jsx```

const [email, setEmail] = useState('invalid-email');

const [error, setError] = useState('Please enter a valid email address');

return (

<s-section>

<s-stack gap="base" justifyContent="start">

<s-text-field label="Name" />

<s-email-field

label="Contact email"

details="We'll send your order confirmation here"

value={email}

error={error}

required

onInput={(e) => {

setEmail(e.currentTarget.value);

setError(/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(e.currentTarget.value) ? '' : 'Please enter a valid email address');

}}

/>

</s-stack>

</s-section>

)

```Was this page helpful?YesNo### Updates- [Developer changelog](/changelog)- [Shopify Editions](https://www.shopify.com/editions)### Business growth- [Shopify Partners Program](https://www.shopify.com/partners?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Shopify App Store](https://apps.shopify.com/?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Shopify Academy](https://www.shopifyacademy.com/page/catalog#role_developer?utm_source=web_dotdev&utm_medium=footer_businessgrowth)### Legal- [Terms of service](https://www.shopify.com/legal/terms?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [API terms of use](https://www.shopify.com/legal/api-terms?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Privacy policy](https://www.shopify.com/legal/privacy?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Partners Program Agreement](https://www.shopify.com/partners/terms?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)### Shopify- [About Shopify](https://www.shopify.com/about?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Shopify Plus](https://www.shopify.com/plus?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Careers](https://www.shopify.com/careers?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Investors](https://investors.shopify.com/home/default.aspx?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Press and media](https://shopify.com/news?shpxid=7db0d4e4-24E8-4087-58FA-7EE470CA745A)