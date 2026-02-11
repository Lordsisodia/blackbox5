---
{
  "fetch": {
    "url": "https://shopify.dev/docs/api/admin-extensions/2026-01/polaris-web-components/forms/datepicker",
    "fetched_at": "2026-02-10T13:29:46.839122",
    "status": 200,
    "size_bytes": 288790
  },
  "metadata": {
    "title": "DatePicker",
    "source": "shopify",
    "category": "polaris-web-components",
    "section": "forms",
    "component": "datepicker"
  }
}
---

# DatePicker

Choose a version:2026-01 latest2025-10 2025-07 2025-04 2025-01 2024-10 2024-07 2024-04 2024-01 2023-10 2026-01latest# DatePickerAsk assistantAllow users to select a specific date or date range.

## [Anchor to datepicker](/docs/api/admin-extensions/latest/polaris-web-components/forms/datepicker#datepicker)DatePicker[Anchor to allow](/docs/api/admin-extensions/latest/polaris-web-components/forms/datepicker#datepicker-propertydetail-allow)allow**allow**string**string**Default: ""**Default: ""**Dates that can be selected.

A comma-separated list of dates, date ranges. Whitespace is allowed after commas.

The default `''` allows all dates.

- Dates in `YYYY-MM-DD` format allow a single date.

- Dates in `YYYY-MM` format allow a whole month.

- Dates in `YYYY` format allow a whole year.

- Ranges are expressed as `start--end`.     - Ranges are inclusive.

If either `start` or `end` is omitted, the range is unbounded in that direction.

- If parts of the date are omitted for `start`, they are assumed to be the minimum possible value.

So `2024--` is equivalent to `2024-01-01--`.

- If parts of the date are omitted for `end`, they are assumed to be the maximum possible value.

So `--2024` is equivalent to `--2024-12-31`.

- Whitespace is allowed either side of `--`.

[Anchor to allowDays](/docs/api/admin-extensions/latest/polaris-web-components/forms/datepicker#datepicker-propertydetail-allowdays)allowDays**allowDays**string**string**Default: ""**Default: ""**Days of the week that can be selected. These intersect with the result of `allow` and `disallow`.

A comma-separated list of days. Whitespace is allowed after commas.

The default `''` has no effect on the result of `allow` and `disallow`.

Days are `sunday`, `monday`, `tuesday`, `wednesday`, `thursday`, `friday`, `saturday`.

[Anchor to defaultValue](/docs/api/admin-extensions/latest/polaris-web-components/forms/datepicker#datepicker-propertydetail-defaultvalue)defaultValue**defaultValue**string**string**Default: ""**Default: ""**Default selected value.

The default means no date is selected.

If the provided value is invalid, no date is selected.

- If `type="single"`, this is a date in `YYYY-MM-DD` format.

- If `type="multiple"`, this is a comma-separated list of dates in `YYYY-MM-DD` format.

- If `type="range"`, this is a range in `YYYY-MM-DD--YYYY-MM-DD` format. The range is inclusive.

[Anchor to defaultView](/docs/api/admin-extensions/latest/polaris-web-components/forms/datepicker#datepicker-propertydetail-defaultview)defaultView**defaultView**string**string**Default month to display in `YYYY-MM` format.

This value is used until `view` is set, either directly or as a result of user interaction.

Defaults to the current month in the user's locale.

[Anchor to disallow](/docs/api/admin-extensions/latest/polaris-web-components/forms/datepicker#datepicker-propertydetail-disallow)disallow**disallow**string**string**Default: ""**Default: ""**Dates that cannot be selected. These subtract from `allow`.

A comma-separated list of dates, date ranges. Whitespace is allowed after commas.

The default `''` has no effect on `allow`.

- Dates in `YYYY-MM-DD` format disallow a single date.

- Dates in `YYYY-MM` format disallow a whole month.

- Dates in `YYYY` format disallow a whole year.

- Ranges are expressed as `start--end`.     - Ranges are inclusive.

If either `start` or `end` is omitted, the range is unbounded in that direction.

- If parts of the date are omitted for `start`, they are assumed to be the minimum possible value.

So `2024--` is equivalent to `2024-01-01--`.

- If parts of the date are omitted for `end`, they are assumed to be the maximum possible value.

So `--2024` is equivalent to `--2024-12-31`.

- Whitespace is allowed either side of `--`.

[Anchor to disallowDays](/docs/api/admin-extensions/latest/polaris-web-components/forms/datepicker#datepicker-propertydetail-disallowdays)disallowDays**disallowDays**string**string**Default: ""**Default: ""**Days of the week that cannot be selected. This subtracts from `allowDays`, and intersects with the result of `allow` and `disallow`.

A comma-separated list of days. Whitespace is allowed after commas.

The default `''` has no effect on `allowDays`.

Days are `sunday`, `monday`, `tuesday`, `wednesday`, `thursday`, `friday`, `saturday`.

[Anchor to name](/docs/api/admin-extensions/latest/polaris-web-components/forms/datepicker#datepicker-propertydetail-name)name**name**string**string**An identifier for the field that is unique within the nearest containing form.

[Anchor to type](/docs/api/admin-extensions/latest/polaris-web-components/forms/datepicker#datepicker-propertydetail-type)type**type**"single" | "range"**"single" | "range"**Default: "single"**Default: "single"**[Anchor to value](/docs/api/admin-extensions/latest/polaris-web-components/forms/datepicker#datepicker-propertydetail-value)value**value**string**string**Default: ""**Default: ""**Current selected value.

The default means no date is selected.

If the provided value is invalid, no date is selected.

Otherwise:

- If `type="single"`, this is a date in `YYYY-MM-DD` format.

- If `type="multiple"`, this is a comma-separated list of dates in `YYYY-MM-DD` format.

- If `type="range"`, this is a range in `YYYY-MM-DD--YYYY-MM-DD` format. The range is inclusive.

[Anchor to view](/docs/api/admin-extensions/latest/polaris-web-components/forms/datepicker#datepicker-propertydetail-view)view**view**string**string**Displayed month in `YYYY-MM` format.

`onViewChange` is called when this value changes.

Defaults to `defaultView`.

## [Anchor to events](/docs/api/admin-extensions/latest/polaris-web-components/forms/datepicker#events)EventsLearn more about [registering events](/docs/api/app-home/using-polaris-components#event-handling).

[Anchor to blur](/docs/api/admin-extensions/latest/polaris-web-components/forms/datepicker#events-propertydetail-blur)blur**blur**CallbackEventListenerCallbackEventListener<typeof tagName> | null**CallbackEventListenerCallbackEventListener<typeof tagName> | null**[Anchor to change](/docs/api/admin-extensions/latest/polaris-web-components/forms/datepicker#events-propertydetail-change)change**change**CallbackEventListenerCallbackEventListener<typeof tagName> | null**CallbackEventListenerCallbackEventListener<typeof tagName> | null**[Anchor to focus](/docs/api/admin-extensions/latest/polaris-web-components/forms/datepicker#events-propertydetail-focus)focus**focus**CallbackEventListenerCallbackEventListener<typeof tagName> | null**CallbackEventListenerCallbackEventListener<typeof tagName> | null**[Anchor to input](/docs/api/admin-extensions/latest/polaris-web-components/forms/datepicker#events-propertydetail-input)input**input**CallbackEventListenerCallbackEventListener<typeof tagName> | null**CallbackEventListenerCallbackEventListener<typeof tagName> | null**[Anchor to viewchange](/docs/api/admin-extensions/latest/polaris-web-components/forms/datepicker#events-propertydetail-viewchange)viewchange**viewchange**CallbackEventListenerCallbackEventListener<typeof tagName> | null**CallbackEventListenerCallbackEventListener<typeof tagName> | null**### CallbackEventListener```

(EventListener & {

(event: CallbackEvent<T>): void;

}) | null

```### CallbackEvent```

Event & {

currentTarget: HTMLElementTagNameMap[T];

}

```ExamplesCodejsxhtmlCopy912345<s-date-picker  view="2025-05"  type="range"  value="2025-05-28--2025-05-31" />## Preview### Examples- #### Codejsx```

<s-date-picker

view="2025-05"

type="range"

value="2025-05-28--2025-05-31"

/>

```html```

<s-date-picker

view="2025-05"

type="range"

value="2025-05-28--2025-05-31"

></s-date-picker>

```- #### Single date selectionDescriptionDemonstrates a date picker configured for selecting a single date with a default value and specific month view.jsx```

<s-date-picker

type="single"

name="delivery-date"

value="2024-01-15"

view="2024-01"

/>

```html```

<s-date-picker

type="single"

name="delivery-date"

value="2024-01-15"

view="2024-01"

></s-date-picker>

```- #### With date restrictionsDescriptionIllustrates how to restrict date selection to a specific date range, preventing selection of past or future dates outside the allowed period.jsx```

<s-date-picker

type="single"

name="appointment-date"

disallow="past"

allow="2024-06-01--2024-06-31"

view="2024-06"

/>

```html```

<!-- Disable past dates and far future dates -->

<s-date-picker

type="single"

name="appointment-date"

disallow="past"

allow="2024-06-01--2024-06-31"

view="2024-06"

></s-date-picker>

```- #### Handling onChange callbacksDescriptionDemonstrates how to handle onChange callbacks for both single and range date pickers, showing how to extract and process the selected values.jsx```

const [dateRange, setDateRange] = useState('2024-01-01--2024-01-31');

const [orderNumber, setOrderNumber] = useState('');

const handleApplyFilters = () => {

console.log('Applying filters:', {

orderNumber,

dateRange

});

}

return (

<s-stack gap="base">

<s-text-field

label="Order number"

placeholder="Search orders..."

value={orderNumber}

onChange={(event) => setOrderNumber(event.currentTarget.value)}

/>

<s-date-picker

type="range"

name="order-date-range"

value={dateRange}

onChange={(event) => setDateRange(event.currentTarget.value)}

view="2024-01"

/>

<s-button onClick={handleApplyFilters}>Apply filters</s-button>

</s-stack>

)

```html```

<form>

<s-text-field

label="Order number"

placeholder="Search orders..."

></s-text-field>

<s-date-picker

type="range"

name="order-date-range"

value="2024-01-01--2024-01-31"

view="2024-01"

></s-date-picker>

<s-button type="submit">Apply filters</s-button>

</form>

```- #### With quick date selectionDescriptionIllustrates a date picker with quick preset buttons and onChange callback to capture user selections and update the displayed value.jsx```

const [value, setValue] = useState('2025-01-01--2025-01-31');

const last7Days = () => {

setValue('2025-01-07--2025-01-13');

}

const last30Days = () => {

setValue('2024-12-14--2025-01-13');

}

const thisMonth = () => {

setValue('2025-01-01--2025-01-31');

}

return (

<s-stack gap="base">

<s-button-group>

<s-button slot="secondary-actions" onClick={last7Days}>Last 7 days</s-button>

<s-button slot="secondary-actions" onClick={last30Days}>Last 30 days</s-button>

<s-button slot="secondary-actions" onClick={thisMonth}>This month</s-button>

</s-button-group>

<s-date-picker

type="range"

name="analytics-period"

id="analytics-picker"

view="2025-01"

value={value}

onChange={(event) => {

console.log('Date range changed:', event.currentTarget.value);

setValue(event.currentTarget.value);

}}

/>

<s-text>Selected range: {value}</s-text>

</s-stack>

)

```html```

<!-- Quick date selection with onChange callback -->

<s-stack gap="base">

<s-button-group>

<s-button slot="secondary-actions" id="last-7-days">Last 7 days</s-button>

<s-button slot="secondary-actions" id="last-30-days">Last 30 days</s-button>

<s-button slot="secondary-actions" id="this-month">This month</s-button>

</s-button-group>

<s-date-picker

type="range"

name="analytics-period"

id="analytics-picker"

value="2025-01-01--2025-01-31"

view="2025-01"

onchange="console.log('Date range changed:', event.currentTarget.value)"

></s-date-picker>

<s-text id="selected-range">

Selected range: 2025-01-01--2025-01-31

</s-text>

</s-stack>

<script>

const picker = document.getElementById('analytics-picker');

const display = document.getElementById('selected-range');

// Handle picker changes

picker.addEventListener('change', (event) => {

display.textContent = `Selected range: ${event.currentTarget.value}`;

});

// Quick selection buttons

document.getElementById('last-7-days').addEventListener('click', () => {

picker.value = '2025-01-07--2025-01-13';

display.textContent = 'Selected range: 2025-01-07--2025-01-13';

});

document.getElementById('last-30-days').addEventListener('click', () => {

picker.value = '2024-12-14--2025-01-13';

display.textContent = 'Selected range: 2024-12-14--2025-01-13';

});

document.getElementById('this-month').addEventListener('click', () => {

picker.value = '2025-01-01--2025-01-31';

display.textContent = 'Selected range: 2025-01-01--2025-01-31';

});

</script>

```## [Anchor to best-practices](/docs/api/admin-extensions/latest/polaris-web-components/forms/datepicker#best-practices)Best practices

- Use smart defaults and highlight common selections

- Don't use to enter a date that is many years in the future or the past

Was this page helpful?YesNo### Updates- [Developer changelog](/changelog)- [Shopify Editions](https://www.shopify.com/editions)### Business growth- [Shopify Partners Program](https://www.shopify.com/partners?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Shopify App Store](https://apps.shopify.com/?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Shopify Academy](https://www.shopifyacademy.com/page/catalog#role_developer?utm_source=web_dotdev&utm_medium=footer_businessgrowth)### Legal- [Terms of service](https://www.shopify.com/legal/terms?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [API terms of use](https://www.shopify.com/legal/api-terms?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Privacy policy](https://www.shopify.com/legal/privacy?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Partners Program Agreement](https://www.shopify.com/partners/terms?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)### Shopify- [About Shopify](https://www.shopify.com/about?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Shopify Plus](https://www.shopify.com/plus?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Careers](https://www.shopify.com/careers?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Investors](https://investors.shopify.com/home/default.aspx?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Press and media](https://shopify.com/news?shpxid=7db0d4e4-24E8-4087-58FA-7EE470CA745A)