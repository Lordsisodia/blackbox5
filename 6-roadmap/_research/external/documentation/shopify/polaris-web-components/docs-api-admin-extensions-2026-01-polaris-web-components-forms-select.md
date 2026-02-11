---
{
  "fetch": {
    "url": "https://shopify.dev/docs/api/admin-extensions/2026-01/polaris-web-components/forms/select",
    "fetched_at": "2026-02-10T13:30:06.039683",
    "status": 200,
    "size_bytes": 356515
  },
  "metadata": {
    "title": "Select",
    "source": "shopify",
    "category": "polaris-web-components",
    "section": "forms",
    "component": "select"
  }
}
---

# Select

Choose a version:2026-01 latest2025-10 2025-07 2025-04 2025-01 2024-10 2024-07 2024-04 2024-01 2023-10 2026-01latest# SelectAsk assistantAllow users to pick one option from a menu. Ideal when presenting four or more choices to keep interfaces uncluttered.

## [Anchor to properties](/docs/api/admin-extensions/latest/polaris-web-components/forms/select#properties)Properties[Anchor to details](/docs/api/admin-extensions/latest/polaris-web-components/forms/select#properties-propertydetail-details)details**details**string**string**Additional text to provide context or guidance for the field. This text is displayed along with the field and its label to offer more information or instructions to the user.

This will also be exposed to screen reader users.

[Anchor to disabled](/docs/api/admin-extensions/latest/polaris-web-components/forms/select#properties-propertydetail-disabled)disabled**disabled**boolean**boolean**Default: false**Default: false**Disables the field, disallowing any interaction.

[Anchor to error](/docs/api/admin-extensions/latest/polaris-web-components/forms/select#properties-propertydetail-error)error**error**string**string**Indicate an error to the user. The field will be given a specific stylistic treatment to communicate problems that have to be resolved immediately.

[Anchor to icon](/docs/api/admin-extensions/latest/polaris-web-components/forms/select#properties-propertydetail-icon)icon**icon**"" | "replace" | "search" | "split" | "link" | "edit" | "product" | "variant" | "collection" | "select" | "info" | "incomplete" | "complete" | "color" | "money" | "order" | "code" | "adjust" | "affiliate" | "airplane" | "alert-bubble" | "alert-circle" | "alert-diamond" | "alert-location" | "alert-octagon" | "alert-octagon-filled" | "alert-triangle" | "alert-triangle-filled" | "align-horizontal-centers" | "app-extension" | "apps" | "archive" | "arrow-down" | "arrow-down-circle" | "arrow-down-right" | "arrow-left" | "arrow-left-circle" | "arrow-right" | "arrow-right-circle" | "arrow-up" | "arrow-up-circle" | "arrow-up-right" | "arrows-in-horizontal" | "arrows-out-horizontal" | "asterisk" | "attachment" | "automation" | "backspace" | "bag" | "bank" | "barcode" | "battery-low" | "bill" | "blank" | "blog" | "bolt" | "bolt-filled" | "book" | "book-open" | "bug" | "bullet" | "business-entity" | "button" | "button-press" | "calculator" | "calendar" | "calendar-check" | "calendar-compare" | "calendar-list" | "calendar-time" | "camera" | "camera-flip" | "caret-down" | "caret-left" | "caret-right" | "caret-up" | "cart" | "cart-abandoned" | "cart-discount" | "cart-down" | "cart-filled" | "cart-sale" | "cart-send" | "cart-up" | "cash-dollar" | "cash-euro" | "cash-pound" | "cash-rupee" | "cash-yen" | "catalog-product" | "categories" | "channels" | "channels-filled" | "chart-cohort" | "chart-donut" | "chart-funnel" | "chart-histogram-first" | "chart-histogram-first-last" | "chart-histogram-flat" | "chart-histogram-full" | "chart-histogram-growth" | "chart-histogram-last" | "chart-histogram-second-last" | "chart-horizontal" | "chart-line" | "chart-popular" | "chart-stacked" | "chart-vertical" | "chat" | "chat-new" | "chat-referral" | "check" | "check-circle" | "check-circle-filled" | "checkbox" | "chevron-down" | "chevron-down-circle" | "chevron-left" | "chevron-left-circle" | "chevron-right" | "chevron-right-circle" | "chevron-up" | "chevron-up-circle" | "circle" | "circle-dashed" | "clipboard" | "clipboard-check" | "clipboard-checklist" | "clock" | "clock-list" | "clock-revert" | "code-add" | "collection-featured" | "collection-list" | "collection-reference" | "color-none" | "compass" | "compose" | "confetti" | "connect" | "content" | "contract" | "corner-pill" | "corner-round" | "corner-square" | "credit-card" | "credit-card-cancel" | "credit-card-percent" | "credit-card-reader" | "credit-card-reader-chip" | "credit-card-reader-tap" | "credit-card-secure" | "credit-card-tap-chip" | "crop" | "currency-convert" | "cursor" | "cursor-banner" | "cursor-option" | "data-presentation" | "data-table" | "database" | "database-add" | "database-connect" | "delete" | "delivered" | "delivery" | "desktop" | "disabled" | "disabled-filled" | "discount" | "discount-add" | "discount-automatic" | "discount-code" | "discount-remove" | "dns-settings" | "dock-floating" | "dock-side" | "domain" | "domain-landing-page" | "domain-new" | "domain-redirect" | "download" | "drag-drop" | "drag-handle" | "drawer" | "duplicate" | "email" | "email-follow-up" | "email-newsletter" | "empty" | "enabled" | "enter" | "envelope" | "envelope-soft-pack" | "eraser" | "exchange" | "exit" | "export" | "external" | "eye-check-mark" | "eye-dropper" | "eye-dropper-list" | "eye-first" | "eyeglasses" | "fav" | "favicon" | "file" | "file-list" | "filter" | "filter-active" | "flag" | "flip-horizontal" | "flip-vertical" | "flower" | "folder" | "folder-add" | "folder-down" | "folder-remove" | "folder-up" | "food" | "foreground" | "forklift" | "forms" | "games" | "gauge" | "geolocation" | "gift" | "gift-card" | "git-branch" | "git-commit" | "git-repository" | "globe" | "globe-asia" | "globe-europe" | "globe-lines" | "globe-list" | "graduation-hat" | "grid" | "hashtag" | "hashtag-decimal" | "hashtag-list" | "heart" | "hide" | "hide-filled" | "home" | "home-filled" | "icons" | "identity-card" | "image" | "image-add" | "image-alt" | "image-explore" | "image-magic" | "image-none" | "image-with-text-overlay" | "images" | "import" | "in-progress" | "incentive" | "incoming" | "info-filled" | "inheritance" | "inventory" | "inventory-edit" | "inventory-list" | "inventory-transfer" | "inventory-updated" | "iq" | "key" | "keyboard" | "keyboard-filled" | "keyboard-hide" | "keypad" | "label-printer" | "language" | "language-translate" | "layout-block" | "layout-buy-button" | "layout-buy-button-horizontal" | "layout-buy-button-vertical" | "layout-column-1" | "layout-columns-2" | "layout-columns-3" | "layout-footer" | "layout-header" | "layout-logo-block" | "layout-popup" | "layout-rows-2" | "layout-section" | "layout-sidebar-left" | "layout-sidebar-right" | "lightbulb" | "link-list" | "list-bulleted" | "list-bulleted-filled" | "list-numbered" | "live" | "live-critical" | "live-none" | "location" | "location-none" | "lock" | "map" | "markets" | "markets-euro" | "markets-rupee" | "markets-yen" | "maximize" | "measurement-size" | "measurement-size-list" | "measurement-volume" | "measurement-volume-list" | "measurement-weight" | "measurement-weight-list" | "media-receiver" | "megaphone" | "mention" | "menu" | "menu-filled" | "menu-horizontal" | "menu-vertical" | "merge" | "metafields" | "metaobject" | "metaobject-list" | "metaobject-reference" | "microphone" | "microphone-muted" | "minimize" | "minus" | "minus-circle" | "mobile" | "money-none" | "money-split" | "moon" | "nature" | "note" | "note-add" | "notification" | "number-one" | "order-batches" | "order-draft" | "order-filled" | "order-first" | "order-fulfilled" | "order-repeat" | "order-unfulfilled" | "orders-status" | "organization" | "outdent" | "outgoing" | "package" | "package-cancel" | "package-fulfilled" | "package-on-hold" | "package-reassign" | "package-returned" | "page" | "page-add" | "page-attachment" | "page-clock" | "page-down" | "page-heart" | "page-list" | "page-reference" | "page-remove" | "page-report" | "page-up" | "pagination-end" | "pagination-start" | "paint-brush-flat" | "paint-brush-round" | "paper-check" | "partially-complete" | "passkey" | "paste" | "pause-circle" | "payment" | "payment-capture" | "payout" | "payout-dollar" | "payout-euro" | "payout-pound" | "payout-rupee" | "payout-yen" | "person" | "person-add" | "person-exit" | "person-filled" | "person-list" | "person-lock" | "person-remove" | "person-segment" | "personalized-text" | "phablet" | "phone" | "phone-down" | "phone-down-filled" | "phone-in" | "phone-out" | "pin" | "pin-remove" | "plan" | "play" | "play-circle" | "plus" | "plus-circle" | "plus-circle-down" | "plus-circle-filled" | "plus-circle-up" | "point-of-sale" | "point-of-sale-register" | "price-list" | "print" | "product-add" | "product-cost" | "product-filled" | "product-list" | "product-reference" | "product-remove" | "product-return" | "product-unavailable" | "profile" | "profile-filled" | "question-circle" | "question-circle-filled" | "radio-control" | "receipt" | "receipt-dollar" | "receipt-euro" | "receipt-folded" | "receipt-paid" | "receipt-pound" | "receipt-refund" | "receipt-rupee" | "receipt-yen" | "receivables" | "redo" | "referral-code" | "refresh" | "remove-background" | "reorder" | "replay" | "reset" | "return" | "reward" | "rocket" | "rotate-left" | "rotate-right" | "sandbox" | "save" | "savings" | "scan-qr-code" | "search-add" | "search-list" | "search-recent" | "search-resource" | "send" | "settings" | "share" | "shield-check-mark" | "shield-none" | "shield-pending" | "shield-person" | "shipping-label" | "shipping-label-cancel" | "shopcodes" | "slideshow" | "smiley-happy" | "smiley-joy" | "smiley-neutral" | "smiley-sad" | "social-ad" | "social-post" | "sort" | "sort-ascending" | "sort-descending" | "sound" | "sports" | "star" | "star-circle" | "star-filled" | "star-half" | "star-list" | "status" | "status-active" | "stop-circle" | "store" | "store-import" | "store-managed" | "store-online" | "sun" | "table" | "table-masonry" | "tablet" | "target" | "tax" | "team" | "text" | "text-align-center" | "text-align-left" | "text-align-right" | "text-block" | "text-bold" | "text-color" | "text-font" | "text-font-list" | "text-grammar" | "text-in-columns" | "text-in-rows" | "text-indent" | "text-indent-remove" | "text-italic" | "text-quote" | "text-title" | "text-underline" | "text-with-image" | "theme" | "theme-edit" | "theme-store" | "theme-template" | "three-d-environment" | "thumbs-down" | "thumbs-up" | "tip-jar" | "toggle-off" | "toggle-on" | "transaction" | "transaction-fee-add" | "transaction-fee-dollar" | "transaction-fee-euro" | "transaction-fee-pound" | "transaction-fee-rupee" | "transaction-fee-yen" | "transfer" | "transfer-in" | "transfer-internal" | "transfer-out" | "truck" | "undo" | "unknown-device" | "unlock" | "upload" | "variant-list" | "video" | "video-list" | "view" | "viewport-narrow" | "viewport-short" | "viewport-tall" | "viewport-wide" | "wallet" | "wand" | "watch" | "wifi" | "work" | "work-list" | "wrench" | "x" | "x-circle" | "x-circle-filled"View more**"" | "replace" | "search" | "split" | "link" | "edit" | "product" | "variant" | "collection" | "select" | "info" | "incomplete" | "complete" | "color" | "money" | "order" | "code" | "adjust" | "affiliate" | "airplane" | "alert-bubble" | "alert-circle" | "alert-diamond" | "alert-location" | "alert-octagon" | "alert-octagon-filled" | "alert-triangle" | "alert-triangle-filled" | "align-horizontal-centers" | "app-extension" | "apps" | "archive" | "arrow-down" | "arrow-down-circle" | "arrow-down-right" | "arrow-left" | "arrow-left-circle" | "arrow-right" | "arrow-right-circle" | "arrow-up" | "arrow-up-circle" | "arrow-up-right" | "arrows-in-horizontal" | "arrows-out-horizontal" | "asterisk" | "attachment" | "automation" | "backspace" | "bag" | "bank" | "barcode" | "battery-low" | "bill" | "blank" | "blog" | "bolt" | "bolt-filled" | "book" | "book-open" | "bug" | "bullet" | "business-entity" | "button" | "button-press" | "calculator" | "calendar" | "calendar-check" | "calendar-compare" | "calendar-list" | "calendar-time" | "camera" | "camera-flip" | "caret-down" | "caret-left" | "caret-right" | "caret-up" | "cart" | "cart-abandoned" | "cart-discount" | "cart-down" | "cart-filled" | "cart-sale" | "cart-send" | "cart-up" | "cash-dollar" | "cash-euro" | "cash-pound" | "cash-rupee" | "cash-yen" | "catalog-product" | "categories" | "channels" | "channels-filled" | "chart-cohort" | "chart-donut" | "chart-funnel" | "chart-histogram-first" | "chart-histogram-first-last" | "chart-histogram-flat" | "chart-histogram-full" | "chart-histogram-growth" | "chart-histogram-last" | "chart-histogram-second-last" | "chart-horizontal" | "chart-line" | "chart-popular" | "chart-stacked" | "chart-vertical" | "chat" | "chat-new" | "chat-referral" | "check" | "check-circle" | "check-circle-filled" | "checkbox" | "chevron-down" | "chevron-down-circle" | "chevron-left" | "chevron-left-circle" | "chevron-right" | "chevron-right-circle" | "chevron-up" | "chevron-up-circle" | "circle" | "circle-dashed" | "clipboard" | "clipboard-check" | "clipboard-checklist" | "clock" | "clock-list" | "clock-revert" | "code-add" | "collection-featured" | "collection-list" | "collection-reference" | "color-none" | "compass" | "compose" | "confetti" | "connect" | "content" | "contract" | "corner-pill" | "corner-round" | "corner-square" | "credit-card" | "credit-card-cancel" | "credit-card-percent" | "credit-card-reader" | "credit-card-reader-chip" | "credit-card-reader-tap" | "credit-card-secure" | "credit-card-tap-chip" | "crop" | "currency-convert" | "cursor" | "cursor-banner" | "cursor-option" | "data-presentation" | "data-table" | "database" | "database-add" | "database-connect" | "delete" | "delivered" | "delivery" | "desktop" | "disabled" | "disabled-filled" | "discount" | "discount-add" | "discount-automatic" | "discount-code" | "discount-remove" | "dns-settings" | "dock-floating" | "dock-side" | "domain" | "domain-landing-page" | "domain-new" | "domain-redirect" | "download" | "drag-drop" | "drag-handle" | "drawer" | "duplicate" | "email" | "email-follow-up" | "email-newsletter" | "empty" | "enabled" | "enter" | "envelope" | "envelope-soft-pack" | "eraser" | "exchange" | "exit" | "export" | "external" | "eye-check-mark" | "eye-dropper" | "eye-dropper-list" | "eye-first" | "eyeglasses" | "fav" | "favicon" | "file" | "file-list" | "filter" | "filter-active" | "flag" | "flip-horizontal" | "flip-vertical" | "flower" | "folder" | "folder-add" | "folder-down" | "folder-remove" | "folder-up" | "food" | "foreground" | "forklift" | "forms" | "games" | "gauge" | "geolocation" | "gift" | "gift-card" | "git-branch" | "git-commit" | "git-repository" | "globe" | "globe-asia" | "globe-europe" | "globe-lines" | "globe-list" | "graduation-hat" | "grid" | "hashtag" | "hashtag-decimal" | "hashtag-list" | "heart" | "hide" | "hide-filled" | "home" | "home-filled" | "icons" | "identity-card" | "image" | "image-add" | "image-alt" | "image-explore" | "image-magic" | "image-none" | "image-with-text-overlay" | "images" | "import" | "in-progress" | "incentive" | "incoming" | "info-filled" | "inheritance" | "inventory" | "inventory-edit" | "inventory-list" | "inventory-transfer" | "inventory-updated" | "iq" | "key" | "keyboard" | "keyboard-filled" | "keyboard-hide" | "keypad" | "label-printer" | "language" | "language-translate" | "layout-block" | "layout-buy-button" | "layout-buy-button-horizontal" | "layout-buy-button-vertical" | "layout-column-1" | "layout-columns-2" | "layout-columns-3" | "layout-footer" | "layout-header" | "layout-logo-block" | "layout-popup" | "layout-rows-2" | "layout-section" | "layout-sidebar-left" | "layout-sidebar-right" | "lightbulb" | "link-list" | "list-bulleted" | "list-bulleted-filled" | "list-numbered" | "live" | "live-critical" | "live-none" | "location" | "location-none" | "lock" | "map" | "markets" | "markets-euro" | "markets-rupee" | "markets-yen" | "maximize" | "measurement-size" | "measurement-size-list" | "measurement-volume" | "measurement-volume-list" | "measurement-weight" | "measurement-weight-list" | "media-receiver" | "megaphone" | "mention" | "menu" | "menu-filled" | "menu-horizontal" | "menu-vertical" | "merge" | "metafields" | "metaobject" | "metaobject-list" | "metaobject-reference" | "microphone" | "microphone-muted" | "minimize" | "minus" | "minus-circle" | "mobile" | "money-none" | "money-split" | "moon" | "nature" | "note" | "note-add" | "notification" | "number-one" | "order-batches" | "order-draft" | "order-filled" | "order-first" | "order-fulfilled" | "order-repeat" | "order-unfulfilled" | "orders-status" | "organization" | "outdent" | "outgoing" | "package" | "package-cancel" | "package-fulfilled" | "package-on-hold" | "package-reassign" | "package-returned" | "page" | "page-add" | "page-attachment" | "page-clock" | "page-down" | "page-heart" | "page-list" | "page-reference" | "page-remove" | "page-report" | "page-up" | "pagination-end" | "pagination-start" | "paint-brush-flat" | "paint-brush-round" | "paper-check" | "partially-complete" | "passkey" | "paste" | "pause-circle" | "payment" | "payment-capture" | "payout" | "payout-dollar" | "payout-euro" | "payout-pound" | "payout-rupee" | "payout-yen" | "person" | "person-add" | "person-exit" | "person-filled" | "person-list" | "person-lock" | "person-remove" | "person-segment" | "personalized-text" | "phablet" | "phone" | "phone-down" | "phone-down-filled" | "phone-in" | "phone-out" | "pin" | "pin-remove" | "plan" | "play" | "play-circle" | "plus" | "plus-circle" | "plus-circle-down" | "plus-circle-filled" | "plus-circle-up" | "point-of-sale" | "point-of-sale-register" | "price-list" | "print" | "product-add" | "product-cost" | "product-filled" | "product-list" | "product-reference" | "product-remove" | "product-return" | "product-unavailable" | "profile" | "profile-filled" | "question-circle" | "question-circle-filled" | "radio-control" | "receipt" | "receipt-dollar" | "receipt-euro" | "receipt-folded" | "receipt-paid" | "receipt-pound" | "receipt-refund" | "receipt-rupee" | "receipt-yen" | "receivables" | "redo" | "referral-code" | "refresh" | "remove-background" | "reorder" | "replay" | "reset" | "return" | "reward" | "rocket" | "rotate-left" | "rotate-right" | "sandbox" | "save" | "savings" | "scan-qr-code" | "search-add" | "search-list" | "search-recent" | "search-resource" | "send" | "settings" | "share" | "shield-check-mark" | "shield-none" | "shield-pending" | "shield-person" | "shipping-label" | "shipping-label-cancel" | "shopcodes" | "slideshow" | "smiley-happy" | "smiley-joy" | "smiley-neutral" | "smiley-sad" | "social-ad" | "social-post" | "sort" | "sort-ascending" | "sort-descending" | "sound" | "sports" | "star" | "star-circle" | "star-filled" | "star-half" | "star-list" | "status" | "status-active" | "stop-circle" | "store" | "store-import" | "store-managed" | "store-online" | "sun" | "table" | "table-masonry" | "tablet" | "target" | "tax" | "team" | "text" | "text-align-center" | "text-align-left" | "text-align-right" | "text-block" | "text-bold" | "text-color" | "text-font" | "text-font-list" | "text-grammar" | "text-in-columns" | "text-in-rows" | "text-indent" | "text-indent-remove" | "text-italic" | "text-quote" | "text-title" | "text-underline" | "text-with-image" | "theme" | "theme-edit" | "theme-store" | "theme-template" | "three-d-environment" | "thumbs-down" | "thumbs-up" | "tip-jar" | "toggle-off" | "toggle-on" | "transaction" | "transaction-fee-add" | "transaction-fee-dollar" | "transaction-fee-euro" | "transaction-fee-pound" | "transaction-fee-rupee" | "transaction-fee-yen" | "transfer" | "transfer-in" | "transfer-internal" | "transfer-out" | "truck" | "undo" | "unknown-device" | "unlock" | "upload" | "variant-list" | "video" | "video-list" | "view" | "viewport-narrow" | "viewport-short" | "viewport-tall" | "viewport-wide" | "wallet" | "wand" | "watch" | "wifi" | "work" | "work-list" | "wrench" | "x" | "x-circle" | "x-circle-filled"View more**The type of icon to be displayed in the field.

[Anchor to id](/docs/api/admin-extensions/latest/polaris-web-components/forms/select#properties-propertydetail-id)id**id**string**string**A unique identifier for the element.

[Anchor to label](/docs/api/admin-extensions/latest/polaris-web-components/forms/select#properties-propertydetail-label)label**label**string**string**Content to use as the field label.

[Anchor to labelAccessibilityVisibility](/docs/api/admin-extensions/latest/polaris-web-components/forms/select#properties-propertydetail-labelaccessibilityvisibility)labelAccessibilityVisibility**labelAccessibilityVisibility**"visible" | "exclusive"**"visible" | "exclusive"**Default: 'visible'**Default: 'visible'**Changes the visibility of the component's label.

- `visible`: the label is visible to all users.

- `exclusive`: the label is visually hidden but remains in the accessibility tree.

[Anchor to name](/docs/api/admin-extensions/latest/polaris-web-components/forms/select#properties-propertydetail-name)name**name**string**string**An identifier for the field that is unique within the nearest containing form.

[Anchor to placeholder](/docs/api/admin-extensions/latest/polaris-web-components/forms/select#properties-propertydetail-placeholder)placeholder**placeholder**string**string**A short hint that describes the expected value of the field.

[Anchor to required](/docs/api/admin-extensions/latest/polaris-web-components/forms/select#properties-propertydetail-required)required**required**boolean**boolean**Default: false**Default: false**Whether the field needs a value. This requirement adds semantic value to the field, but it will not cause an error to appear automatically. If you want to present an error when this field is empty, you can do so with the `error` property.

[Anchor to value](/docs/api/admin-extensions/latest/polaris-web-components/forms/select#properties-propertydetail-value)value**value**string**string**The current value for the field. If omitted, the field will be empty.

## [Anchor to events](/docs/api/admin-extensions/latest/polaris-web-components/forms/select#events)EventsLearn more about [registering events](/docs/api/app-home/using-polaris-components#event-handling).

[Anchor to change](/docs/api/admin-extensions/latest/polaris-web-components/forms/select#events-propertydetail-change)change**change**CallbackEventListenerCallbackEventListener<'input'>**CallbackEventListenerCallbackEventListener<'input'>**[Anchor to input](/docs/api/admin-extensions/latest/polaris-web-components/forms/select#events-propertydetail-input)input**input**CallbackEventListenerCallbackEventListener<'input'>**CallbackEventListenerCallbackEventListener<'input'>**### CallbackEventListener```

(EventListener & {

(event: CallbackEvent<T>): void;

}) | null

```### CallbackEvent```

Event & {

currentTarget: HTMLElementTagNameMap[T];

}

```## [Anchor to slots](/docs/api/admin-extensions/latest/polaris-web-components/forms/select#slots)Slots[Anchor to children](/docs/api/admin-extensions/latest/polaris-web-components/forms/select#slots-propertydetail-children)children**children**HTMLElement**HTMLElement**The options a user can select from.

Accepts `Option` and `OptionGroup` components.

## [Anchor to option](/docs/api/admin-extensions/latest/polaris-web-components/forms/select#option)OptionRepresents a single option within a select component. Use only as a child of `s-select` components.

[Anchor to defaultSelected](/docs/api/admin-extensions/latest/polaris-web-components/forms/select#option-propertydetail-defaultselected)defaultSelected**defaultSelected**boolean**boolean**Default: false**Default: false**Whether the control is active by default.

[Anchor to disabled](/docs/api/admin-extensions/latest/polaris-web-components/forms/select#option-propertydetail-disabled)disabled**disabled**boolean**boolean**Default: false**Default: false**Disables the control, disallowing any interaction.

[Anchor to selected](/docs/api/admin-extensions/latest/polaris-web-components/forms/select#option-propertydetail-selected)selected**selected**boolean**boolean**Default: false**Default: false**Whether the control is active.

[Anchor to value](/docs/api/admin-extensions/latest/polaris-web-components/forms/select#option-propertydetail-value)value**value**string**string**The value used in form data when the control is checked.

## [Anchor to slots](/docs/api/admin-extensions/latest/polaris-web-components/forms/select#slots)Slots[Anchor to children](/docs/api/admin-extensions/latest/polaris-web-components/forms/select#slots-propertydetail-children)children**children**HTMLElement**HTMLElement**The content to use as the label.

## [Anchor to optiongroup](/docs/api/admin-extensions/latest/polaris-web-components/forms/select#optiongroup)OptionGroupRepresents a group of options within a select component. Use only as a child of `s-select` components.

[Anchor to disabled](/docs/api/admin-extensions/latest/polaris-web-components/forms/select#optiongroup-propertydetail-disabled)disabled**disabled**boolean**boolean**Default: false**Default: false**Whether the options within this group can be selected or not.

[Anchor to label](/docs/api/admin-extensions/latest/polaris-web-components/forms/select#optiongroup-propertydetail-label)label**label**string**string**The user-facing label for this group of options.

## [Anchor to slots](/docs/api/admin-extensions/latest/polaris-web-components/forms/select#slots)Slots[Anchor to children](/docs/api/admin-extensions/latest/polaris-web-components/forms/select#slots-propertydetail-children)children**children**HTMLElement**HTMLElement**The options a user can select from.

Accepts `Option` components.

ExamplesCodejsxhtmlCopy9123456789<s-select label="Date range">  <s-option value="1">Today</s-option>  <s-option value="2">Yesterday</s-option>  <s-option value="3">Last 7 days</s-option>  <s-option-group label="Custom ranges">    <s-option value="4">Last 30 days</s-option>    <s-option value="5">Last 90 days</s-option>  </s-option-group></s-select>## Preview### Examples- #### Codejsx```

<s-select label="Date range">

<s-option value="1">Today</s-option>

<s-option value="2">Yesterday</s-option>

<s-option value="3">Last 7 days</s-option>

<s-option-group label="Custom ranges">

<s-option value="4">Last 30 days</s-option>

<s-option value="5">Last 90 days</s-option>

</s-option-group>

</s-select>

```html```

<s-select label="Date range">

<s-option value="1">Today</s-option>

<s-option value="2">Yesterday</s-option>

<s-option value="3">Last 7 days</s-option>

<s-option-group label="Custom ranges">

<s-option value="4">Last 30 days</s-option>

<s-option value="5">Last 90 days</s-option>

</s-option-group>

</s-select>

```- #### Basic usageDescriptionA simple select dropdown with pre-selected value for product sorting options.jsx```

<s-select label="Sort products by" value="newest">

<s-option value="newest">Newest first</s-option>

<s-option value="oldest">Oldest first</s-option>

<s-option value="title">Title A–Z</s-option>

<s-option value="price-low">Price: low to high</s-option>

<s-option value="price-high">Price: high to low</s-option>

</s-select>

```html```

<s-select label="Sort products by" value="newest">

<s-option value="newest">Newest first</s-option>

<s-option value="oldest">Oldest first</s-option>

<s-option value="title">Title A–Z</s-option>

<s-option value="price-low">Price: low to high</s-option>

<s-option value="price-high">Price: high to low</s-option>

</s-select>

```- #### With placeholderDescriptionSelect dropdown with helpful placeholder text guiding category selection.jsx```

<s-select

label="Product category"

placeholder="Choose category for better organization"

>

<s-option value="clothing">Clothing & apparel</s-option>

<s-option value="accessories">Accessories & jewelry</s-option>

<s-option value="home-garden">Home & garden</s-option>

<s-option value="electronics">Electronics & tech</s-option>

<s-option value="books">Books & media</s-option>

</s-select>

```html```

<s-select

label="Product category"

placeholder="Choose category for better organization"

>

<s-option value="clothing">Clothing & apparel</s-option>

<s-option value="accessories">Accessories & jewelry</s-option>

<s-option value="home-garden">Home & garden</s-option>

<s-option value="electronics">Electronics & tech</s-option>

<s-option value="books">Books & media</s-option>

</s-select>

```- #### With error stateDescriptionSelect in error state showing specific business context and actionable error message.jsx```

<s-select

label="Shipping origin"

error="Select your primary shipping location to calculate accurate rates for customers"

required

>

<s-option value="ca">Canada</s-option>

<s-option value="us">United states</s-option>

<s-option value="mx">Mexico</s-option>

<s-option value="uk">United kingdom</s-option>

</s-select>

```html```

<s-select

label="Shipping origin"

error="Select your primary shipping location to calculate accurate rates for customers"

required

>

<s-option value="ca">Canada</s-option>

<s-option value="us">United states</s-option>

<s-option value="mx">Mexico</s-option>

<s-option value="uk">United kingdom</s-option>

</s-select>

```- #### With option groupsDescriptionGrouped select options organized by geographical regions for international shipping.jsx```

<s-select label="Shipping destination">

<s-option-group label="North america">

<s-option value="ca">Canada</s-option>

<s-option value="us">United states</s-option>

<s-option value="mx">Mexico</s-option>

</s-option-group>

<s-option-group label="Europe">

<s-option value="uk">United kingdom</s-option>

<s-option value="fr">France</s-option>

<s-option value="de">Germany</s-option>

<s-option value="it">Italy</s-option>

</s-option-group>

<s-option-group label="Asia pacific">

<s-option value="au">Australia</s-option>

<s-option value="jp">Japan</s-option>

<s-option value="sg">Singapore</s-option>

</s-option-group>

</s-select>

```html```

<s-select label="Shipping destination">

<s-option-group label="North america">

<s-option value="ca">Canada</s-option>

<s-option value="us">United states</s-option>

<s-option value="mx">Mexico</s-option>

</s-option-group>

<s-option-group label="Europe">

<s-option value="uk">United kingdom</s-option>

<s-option value="fr">France</s-option>

<s-option value="de">Germany</s-option>

<s-option value="it">Italy</s-option>

</s-option-group>

<s-option-group label="Asia pacific">

<s-option value="au">Australia</s-option>

<s-option value="jp">Japan</s-option>

<s-option value="sg">Singapore</s-option>

</s-option-group>

</s-select>

```- #### With iconDescriptionSelect dropdown with sort icon for filtering order management views.jsx```

<s-select label="Filter orders by" icon="sort">

<s-option value="date">Order date</s-option>

<s-option value="status">Fulfillment status</s-option>

<s-option value="total">Order total</s-option>

<s-option value="customer">Customer name</s-option>

</s-select>

```html```

<s-select label="Filter orders by" icon="sort">

<s-option value="date">Order date</s-option>

<s-option value="status">Fulfillment status</s-option>

<s-option value="total">Order total</s-option>

<s-option value="customer">Customer name</s-option>

</s-select>

```- #### Disabled stateDescriptionSelect in disabled state preventing user interaction with pre-selected value.jsx```

<s-select label="Product type" disabled value="physical">

<s-option value="physical">Physical product</s-option>

<s-option value="digital">Digital product</s-option>

<s-option value="service">Service</s-option>

<s-option value="gift-card">Gift card</s-option>

</s-select>

```html```

<s-select label="Product type" disabled value="physical">

<s-option value="physical">Physical product</s-option>

<s-option value="digital">Digital product</s-option>

<s-option value="service">Service</s-option>

<s-option value="gift-card">Gift card</s-option>

</s-select>

```Was this page helpful?YesNo### Updates- [Developer changelog](/changelog)- [Shopify Editions](https://www.shopify.com/editions)### Business growth- [Shopify Partners Program](https://www.shopify.com/partners?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Shopify App Store](https://apps.shopify.com/?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Shopify Academy](https://www.shopifyacademy.com/page/catalog#role_developer?utm_source=web_dotdev&utm_medium=footer_businessgrowth)### Legal- [Terms of service](https://www.shopify.com/legal/terms?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [API terms of use](https://www.shopify.com/legal/api-terms?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Privacy policy](https://www.shopify.com/legal/privacy?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Partners Program Agreement](https://www.shopify.com/partners/terms?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)### Shopify- [About Shopify](https://www.shopify.com/about?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Shopify Plus](https://www.shopify.com/plus?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Careers](https://www.shopify.com/careers?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Investors](https://investors.shopify.com/home/default.aspx?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Press and media](https://shopify.com/news?shpxid=7db0d4e4-24E8-4087-58FA-7EE470CA745A)