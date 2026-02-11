---
{
  "fetch": {
    "url": "https://shopify.dev/docs/api/admin-extensions/2026-01/polaris-web-components/forms/urlfield",
    "fetched_at": "2026-02-10T13:30:23.820405",
    "status": 200,
    "size_bytes": 289679
  },
  "metadata": {
    "title": "URLField",
    "source": "shopify",
    "category": "polaris-web-components",
    "section": "forms",
    "component": "urlfield"
  }
}
---

# URLField

Choose a version:2026-01 latest2025-10 2025-07 2025-04 2025-01 2024-10 2024-07 2024-04 2024-01 2023-10 2026-01latest# URLFieldAsk assistantCollect URLs from users with built-in formatting and validation.

## [Anchor to urlfield](/docs/api/admin-extensions/latest/polaris-web-components/forms/urlfield#urlfield)URLField[Anchor to autocomplete](/docs/api/admin-extensions/latest/polaris-web-components/forms/urlfield#urlfield-propertydetail-autocomplete)autocomplete**autocomplete**"on" | "off" | `section-${string} url` | `section-${string} photo` | `section-${string} impp` | `section-${string} home impp` | `section-${string} mobile impp` | `section-${string} fax impp` | `section-${string} pager impp` | "shipping url" | "shipping photo" | "shipping impp" | "shipping home impp" | "shipping mobile impp" | "shipping fax impp" | "shipping pager impp" | "billing url" | "billing photo" | "billing impp" | "billing home impp" | "billing mobile impp" | "billing fax impp" | "billing pager impp" | `section-${string} shipping url` | `section-${string} shipping photo` | `section-${string} shipping impp` | `section-${string} shipping home impp` | `section-${string} shipping mobile impp` | `section-${string} shipping fax impp` | `section-${string} shipping pager impp` | `section-${string} billing url` | `section-${string} billing photo` | `section-${string} billing impp` | `section-${string} billing home impp` | `section-${string} billing mobile impp` | `section-${string} billing fax impp` | `section-${string} billing pager impp` | URLAutocompleteFieldURLAutocompleteField**"on" | "off" | `section-${string} url` | `section-${string} photo` | `section-${string} impp` | `section-${string} home impp` | `section-${string} mobile impp` | `section-${string} fax impp` | `section-${string} pager impp` | "shipping url" | "shipping photo" | "shipping impp" | "shipping home impp" | "shipping mobile impp" | "shipping fax impp" | "shipping pager impp" | "billing url" | "billing photo" | "billing impp" | "billing home impp" | "billing mobile impp" | "billing fax impp" | "billing pager impp" | `section-${string} shipping url` | `section-${string} shipping photo` | `section-${string} shipping impp` | `section-${string} shipping home impp` | `section-${string} shipping mobile impp` | `section-${string} shipping fax impp` | `section-${string} shipping pager impp` | `section-${string} billing url` | `section-${string} billing photo` | `section-${string} billing impp` | `section-${string} billing home impp` | `section-${string} billing mobile impp` | `section-${string} billing fax impp` | `section-${string} billing pager impp` | URLAutocompleteFieldURLAutocompleteField**Default: 'on' for everything else**Default: 'on' for everything else**A hint as to the intended content of the field.

When set to `on` (the default), this property indicates that the field should support autofill, but you do not have any more semantic information on the intended contents.

When set to `off`, you are indicating that this field contains sensitive information, or contents that are never saved, like one-time codes.

Alternatively, you can provide value which describes the specific data you would like to be entered into this field during autofill.

[Anchor to defaultValue](/docs/api/admin-extensions/latest/polaris-web-components/forms/urlfield#urlfield-propertydetail-defaultvalue)defaultValue**defaultValue**string**string**The default value for the field.

[Anchor to details](/docs/api/admin-extensions/latest/polaris-web-components/forms/urlfield#urlfield-propertydetail-details)details**details**string**string**Additional text to provide context or guidance for the field. This text is displayed along with the field and its label to offer more information or instructions to the user.

This will also be exposed to screen reader users.

[Anchor to disabled](/docs/api/admin-extensions/latest/polaris-web-components/forms/urlfield#urlfield-propertydetail-disabled)disabled**disabled**boolean**boolean**Default: false**Default: false**Disables the field, disallowing any interaction.

[Anchor to error](/docs/api/admin-extensions/latest/polaris-web-components/forms/urlfield#urlfield-propertydetail-error)error**error**string**string**Indicate an error to the user. The field will be given a specific stylistic treatment to communicate problems that have to be resolved immediately.

[Anchor to id](/docs/api/admin-extensions/latest/polaris-web-components/forms/urlfield#urlfield-propertydetail-id)id**id**string**string**A unique identifier for the element.

[Anchor to label](/docs/api/admin-extensions/latest/polaris-web-components/forms/urlfield#urlfield-propertydetail-label)label**label**string**string**Content to use as the field label.

[Anchor to labelAccessibilityVisibility](/docs/api/admin-extensions/latest/polaris-web-components/forms/urlfield#urlfield-propertydetail-labelaccessibilityvisibility)labelAccessibilityVisibility**labelAccessibilityVisibility**"visible" | "exclusive"**"visible" | "exclusive"**Default: 'visible'**Default: 'visible'**Changes the visibility of the component's label.

- `visible`: the label is visible to all users.

- `exclusive`: the label is visually hidden but remains in the accessibility tree.

[Anchor to maxLength](/docs/api/admin-extensions/latest/polaris-web-components/forms/urlfield#urlfield-propertydetail-maxlength)maxLength**maxLength**number**number**Default: Infinity**Default: Infinity**Specifies the maximum number of characters allowed.

[Anchor to minLength](/docs/api/admin-extensions/latest/polaris-web-components/forms/urlfield#urlfield-propertydetail-minlength)minLength**minLength**number**number**Default: 0**Default: 0**Specifies the min number of characters allowed.

[Anchor to name](/docs/api/admin-extensions/latest/polaris-web-components/forms/urlfield#urlfield-propertydetail-name)name**name**string**string**An identifier for the field that is unique within the nearest containing form.

[Anchor to placeholder](/docs/api/admin-extensions/latest/polaris-web-components/forms/urlfield#urlfield-propertydetail-placeholder)placeholder**placeholder**string**string**A short hint that describes the expected value of the field.

[Anchor to readOnly](/docs/api/admin-extensions/latest/polaris-web-components/forms/urlfield#urlfield-propertydetail-readonly)readOnly**readOnly**boolean**boolean**Default: false**Default: false**The field cannot be edited by the user. It is focusable will be announced by screen readers.

[Anchor to required](/docs/api/admin-extensions/latest/polaris-web-components/forms/urlfield#urlfield-propertydetail-required)required**required**boolean**boolean**Default: false**Default: false**Whether the field needs a value. This requirement adds semantic value to the field, but it will not cause an error to appear automatically. If you want to present an error when this field is empty, you can do so with the `error` property.

[Anchor to value](/docs/api/admin-extensions/latest/polaris-web-components/forms/urlfield#urlfield-propertydetail-value)value**value**string**string**The current value for the field. If omitted, the field will be empty.

### URLAutocompleteField```

'url' | 'photo' | 'impp' | 'home impp' | 'mobile impp' | 'fax impp' | 'pager impp'

```## [Anchor to events](/docs/api/admin-extensions/latest/polaris-web-components/forms/urlfield#events)EventsLearn more about [registering events](/docs/api/app-home/using-polaris-components#event-handling).

[Anchor to blur](/docs/api/admin-extensions/latest/polaris-web-components/forms/urlfield#events-propertydetail-blur)blur**blur**CallbackEventListenerCallbackEventListener<'input'>**CallbackEventListenerCallbackEventListener<'input'>**[Anchor to change](/docs/api/admin-extensions/latest/polaris-web-components/forms/urlfield#events-propertydetail-change)change**change**CallbackEventListenerCallbackEventListener<'input'>**CallbackEventListenerCallbackEventListener<'input'>**[Anchor to focus](/docs/api/admin-extensions/latest/polaris-web-components/forms/urlfield#events-propertydetail-focus)focus**focus**CallbackEventListenerCallbackEventListener<'input'>**CallbackEventListenerCallbackEventListener<'input'>**[Anchor to input](/docs/api/admin-extensions/latest/polaris-web-components/forms/urlfield#events-propertydetail-input)input**input**CallbackEventListenerCallbackEventListener<'input'>**CallbackEventListenerCallbackEventListener<'input'>**### CallbackEventListener```

(EventListener & {

(event: CallbackEvent<T>): void;

}) | null

```### CallbackEvent```

Event & {

currentTarget: HTMLElementTagNameMap[T];

}

```ExamplesCodejsxhtmlCopy912345<s-url-field  label="Your website"  details="Join the partner ecosystem"  placeholder="https://shopify.com/partner" />## Preview### Examples- #### Codejsx```

<s-url-field

label="Your website"

details="Join the partner ecosystem"

placeholder="https://shopify.com/partner"

/>

```html```

<s-url-field

label="Your website"

details="Join the partner ecosystem"

placeholder="https://shopify.com/partner"

></s-url-field>

```- #### Basic usageDescriptionDemonstrates a simple URL input field with a label and placeholder, showing the minimal configuration needed for collecting a URL.jsx```

<s-stack gap="base">

{/* Simple URL input */}

<s-url-field

label="Website URL"

placeholder="https://example.com"

/>

</s-stack>

```html```

<s-stack gap="base">

<!-- Simple URL input -->

<s-url-field

label="Website URL"

placeholder="https://example.com"

></s-url-field>

</s-stack>

```- #### With validationDescriptionShows a URL input field with built-in validation, including required status, minimum and maximum length constraints, and a custom error message for invalid inputs.jsx```

<s-url-field

label="Company website"

required

minLength={10}

maxLength={200}

error="Please enter a valid website URL"

/>

```html```

<s-url-field

label="Company website"

required

minLength="10"

maxLength="200"

error="Please enter a valid website URL"

></s-url-field>

```- #### With default valueDescriptionIllustrates a URL field pre-populated with a default value, set to read-only mode to prevent user modifications.jsx```

<s-stack gap="base">

<s-url-field

label="Profile URL"

defaultValue="https://shop.myshopify.com"

readOnly

/>

</s-stack>

```html```

<s-stack gap="base">

<s-url-field

label="Profile URL"

value="https://shop.myshopify.com"

readOnly

></s-url-field>

</s-stack>

```- #### Disabled stateDescriptionShows a URL field in a disabled state, displaying a pre-filled URL that cannot be edited by the user.jsx```

<s-url-field

label="Store URL"

value="https://your-store.myshopify.com"

disabled

/>

```html```

<s-url-field

label="Store URL"

value="https://your-store.myshopify.com"

disabled

></s-url-field>

```Was this page helpful?YesNo### Updates- [Developer changelog](/changelog)- [Shopify Editions](https://www.shopify.com/editions)### Business growth- [Shopify Partners Program](https://www.shopify.com/partners?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Shopify App Store](https://apps.shopify.com/?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Shopify Academy](https://www.shopifyacademy.com/page/catalog#role_developer?utm_source=web_dotdev&utm_medium=footer_businessgrowth)### Legal- [Terms of service](https://www.shopify.com/legal/terms?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [API terms of use](https://www.shopify.com/legal/api-terms?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Privacy policy](https://www.shopify.com/legal/privacy?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Partners Program Agreement](https://www.shopify.com/partners/terms?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)### Shopify- [About Shopify](https://www.shopify.com/about?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Shopify Plus](https://www.shopify.com/plus?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Careers](https://www.shopify.com/careers?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Investors](https://investors.shopify.com/home/default.aspx?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Press and media](https://shopify.com/news?shpxid=7db0d4e4-24E8-4087-58FA-7EE470CA745A)