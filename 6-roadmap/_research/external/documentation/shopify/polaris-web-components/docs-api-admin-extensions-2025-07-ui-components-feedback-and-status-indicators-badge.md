---
{
  "fetch": {
    "url": "https://shopify.dev/docs/api/admin-extensions/2025-07/ui-components/feedback-and-status-indicators/badge",
    "fetched_at": "2026-02-10T13:28:28.437646",
    "status": 200,
    "size_bytes": 272111
  },
  "metadata": {
    "title": "Badge",
    "source": "shopify",
    "category": "polaris-web-components",
    "section": "feedback-and-status-indicators",
    "component": "badge"
  }
}
---

# Badge

Choose a version:2026-01 latest2025-10 2025-07 2025-04 2025-01 2024-10 2024-07 2024-04 2024-01 2023-10 2025-07# BadgeAsk assistantUse this component to inform merchants of the status of an object or of an action that’s been taken.

## [Anchor to badgeprops](/docs/api/admin-extensions/2025-07/ui-components/feedback-and-status-indicators/badge#badgeprops)BadgeProps`[BadgeBaseProps](#BadgeBaseProps) & ([BadgeIconProps](#BadgeIconProps) | [BadgeNoIconProps](#BadgeNoIconProps))`**`[BadgeBaseProps](#BadgeBaseProps) & ([BadgeIconProps](#BadgeIconProps) | [BadgeNoIconProps](#BadgeNoIconProps))`**[Anchor to BadgeBaseProps](/docs/api/admin-extensions/2025-07/ui-components/feedback-and-status-indicators/badge#badgeprops-badgebaseprops)### BadgeBaseProps[Anchor to accessibilityLabel](/docs/api/admin-extensions/2025-07/ui-components/feedback-and-status-indicators/badge#badgeprops-propertydetail-accessibilitylabel)accessibilityLabel**accessibilityLabel**string**string**A label that describes the purpose or contents of the element. When set, it will be announced to users using assistive technologies and will provide them with more context. When set, any children or `label` supplied will not be announced to screen readers.

[Anchor to size](/docs/api/admin-extensions/2025-07/ui-components/feedback-and-status-indicators/badge#badgeprops-propertydetail-size)size**size**'base' | 'small-100'**'base' | 'small-100'**Adjusts the size of the badge.

[Anchor to tone](/docs/api/admin-extensions/2025-07/ui-components/feedback-and-status-indicators/badge#badgeprops-propertydetail-tone)tone**tone**ToneTone**ToneTone**Adjusts the color of the badge.

[Anchor to BadgeIconProps](/docs/api/admin-extensions/2025-07/ui-components/feedback-and-status-indicators/badge#badgeprops-badgeiconprops)### BadgeIconProps[Anchor to icon](/docs/api/admin-extensions/2025-07/ui-components/feedback-and-status-indicators/badge#badgeprops-propertydetail-icon)icon**icon**IconNameIconName**IconNameIconName**required**required**Adds an icon to the badge.

[Anchor to iconPosition](/docs/api/admin-extensions/2025-07/ui-components/feedback-and-status-indicators/badge#badgeprops-propertydetail-iconposition)iconPosition**iconPosition**'start' | 'end'**'start' | 'end'**Default: 'start'**Default: 'start'**Adjusts the position of the icon within the badge. Requires `icon` to be set.

[Anchor to BadgeNoIconProps](/docs/api/admin-extensions/2025-07/ui-components/feedback-and-status-indicators/badge#badgeprops-badgenoiconprops)### BadgeNoIconProps[Anchor to icon](/docs/api/admin-extensions/2025-07/ui-components/feedback-and-status-indicators/badge#badgeprops-propertydetail-icon)icon**icon**never**never**[Anchor to iconPosition](/docs/api/admin-extensions/2025-07/ui-components/feedback-and-status-indicators/badge#badgeprops-propertydetail-iconposition)iconPosition**iconPosition**never**never**### BadgeBaseProps- accessibilityLabelA label that describes the purpose or contents of the element. When set, it will be announced to users using assistive technologies and will provide them with more context. When set, any children or `label` supplied will not be announced to screen readers.```

string

```- sizeAdjusts the size of the badge.```

'base' | 'small-100'

```- toneAdjusts the color of the badge.```

Tone

``````

interface BadgeBaseProps extends AccessibilityLabelProps {

/**

* Adjusts the color of the badge.

*/

tone?: Tone;

/**

* Adjusts the size of the badge.

*/

size?: Extract<SizeScale, 'small-100' | 'base'>;

}

```### Tone```

'info' | 'success' | 'warning' | 'critical'

```### BadgeIconProps- iconAdds an icon to the badge.```

IconName

```- iconPositionAdjusts the position of the icon within the badge. Requires `icon` to be set.```

'start' | 'end'

``````

interface BadgeIconProps {

/**

* Adds an icon to the badge.

*/

icon: IconName;

/**

* Adjusts the position of the icon within the badge. Requires `icon` to be set.

*

* @defaultValue 'start'

*/

iconPosition?: 'start' | 'end';

}

```### IconName```

'AbandonedCartFilledMajor' | 'AbandonedCartMajor' | 'AccessibilityMajor' | 'ActivitiesMajor' | 'AddCodeMajor' | 'AddImageMajor' | 'AddMajor' | 'AddNoteMajor' | 'AddProductMajor' | 'AdjustMinor' | 'AffiliateMajor' | 'AlertMinor' | 'AnalyticsBarHorizontalMinor' | 'AnalyticsBarStackedMinor' | 'AnalyticsCohortMinor' | 'AnalyticsDonutMinor' | 'AnalyticsFilledMinor' | 'AnalyticsFunnelMinor' | 'AnalyticsLineMinor' | 'AnalyticsMajor' | 'AnalyticsMinor' | 'AnalyticsTableMinor' | 'AnyClickModelMinor' | 'AppExtensionMinor' | 'AppsFilledMajor' | 'AppsMajor' | 'AppsMinor' | 'ArchiveMajor' | 'ArchiveMinor' | 'ArrowDownMinor' | 'ArrowLeftMinor' | 'ArrowRightMinor' | 'ArrowUpMinor' | 'AttachmentFilledMajor' | 'AttachmentMajor' | 'AutomationFilledMajor' | 'AutomationMajor' | 'BackspaceMajor' | 'BalanceFilledMajor' | 'BalanceMajor' | 'BankFilledMajor' | 'BankMajor' | 'BarcodeMajor' | 'BehaviorFilledMajor' | 'BehaviorMajor' | 'BehaviorMinor' | 'BillingStatementDollarFilledMajor' | 'BillingStatementDollarMajor' | 'BillingStatementEuroFilledMajor' | 'BillingStatementEuroMajor' | 'BillingStatementPoundFilledMajor' | 'BillingStatementPoundMajor' | 'BillingStatementRupeeFilledMajor' | 'BillingStatementRupeeMajor' | 'BillingStatementYenFilledMajor' | 'BillingStatementYenMajor' | 'BlockMinor' | 'BlockquoteMajor' | 'BlogMajor' | 'BoldMajor' | 'BoldMinor' | 'BugMajor' | 'ButtonCornerPillMajor' | 'ButtonCornerRoundedMajor' | 'ButtonCornerSquareMajor' | 'ButtonMinor' | 'BuyButtonButtonLayoutMajor' | 'BuyButtonHorizontalLayoutMajor' | 'BuyButtonMajor' | 'BuyButtonVerticalLayoutMajor' | 'CalendarMajor' | 'CalendarMinor' | 'CalendarTickMajor' | 'CalendarTimeMinor' | 'CameraMajor' | 'CancelMajor' | 'CancelMinor' | 'CancelSmallMinor' | 'CapitalFilledMajor' | 'CapitalMajor' | 'CapturePaymentMinor' | 'CardReaderChipMajor' | 'CardReaderMajor' | 'CardReaderTapMajor' | 'CaretDownMinor' | 'CaretUpMinor' | 'CartDownFilledMajor' | 'CartDownMajor' | 'CartFilledMajor' | 'CartMajor' | 'CartUpMajor' | 'CashDollarFilledMajor' | 'CashDollarMajor' | 'CashDollarMinor' | 'CashEuroMajor' | 'CashPoundMajor' | 'CashRupeeMajor' | 'CashYenMajor' | 'CategoriesMajor' | 'ChannelsMajor' | 'ChatMajor' | 'ChecklistAlternateMajor' | 'ChecklistMajor' | 'CheckoutMajor' | 'ChevronDownMinor' | 'ChevronLeftMinor' | 'ChevronRightMinor' | 'ChevronUpMinor' | 'CircleAlertMajor' | 'CircleCancelMajor' | 'CircleCancelMinor' | 'CircleChevronDownMinor' | 'CircleChevronLeftMinor' | 'CircleChevronRightMinor' | 'CircleChevronUpMinor' | 'CircleDisableMinor' | 'CircleDisabledMajor' | 'CircleDotsMajor' | 'CircleDownMajor' | 'CircleInformationMajor' | 'CircleLeftMajor' | 'CircleMinusMajor' | 'CircleMinusMinor' | 'CircleMinusOutlineMinor' | 'CirclePlusMajor' | 'CirclePlusMinor' | 'CirclePlusOutlineMinor' | 'CircleRightMajor' | 'CircleTickMajor' | 'CircleTickMinor' | 'CircleTickOutlineMinor' | 'CircleUpMajor' | 'ClipboardMinor' | 'ClockMajor' | 'ClockMinor' | 'CodeMajor' | 'CodeMinor' | 'CollectionReferenceMinor' | 'CollectionsFilledMajor' | 'CollectionsMajor' | 'ColorNoneMinor' | 'ColorsMajor' | 'Column1Major' | 'ColumnWithTextMajor' | 'Columns2Major' | 'Columns3Major' | 'Columns3Minor' | 'ComposeMajor' | 'ConfettiMajor' | 'ConnectMinor' | 'ContentFilledMinor' | 'ContentMinor' | 'ConversationMinor' | 'CreditCardCancelMajor' | 'CreditCardMajor' | 'CreditCardPercentMajor' | 'CreditCardSecureMajor' | 'CurrencyConvertMinor' | 'CustomerMinusMajor' | 'CustomerPlusMajor' | 'CustomersFilledMinor' | 'CustomersMajor' | 'CustomersMinor' | 'DataDrivenModelMinor' | 'DataVisualizationMajor' | 'DecimalMinor' | 'DeleteMajor' | 'DeleteMinor' | 'DesktopMajor' | 'DetailedPopUpMajor' | 'DiamondAlertMajor' | 'DiamondAlertMinor' | 'DigitalMediaReceiverMajor' | 'DiscountAutomaticMajor' | 'DiscountCodeMajor' | 'DiscountsFilledMinor' | 'DiscountsMajor' | 'DiscountsMinor' | 'DisputeMinor' | 'DnsSettingsMajor' | 'DockFloatingMajor' | 'DockSideMajor' | 'DomainNewMajor' | 'DomainRedirectMinor' | 'DomainsFilledMajor' | 'DomainsMajor' | 'DraftOrdersFilledMajor' | 'DraftOrdersMajor' | 'DragDropMajor' | 'DragHandleMinor' | 'DropdownMinor' | 'DuplicateMinor' | 'DynamicSourceMajor' | 'DynamicSourceMinor' | 'EditMajor' | 'EditMinor' | 'EmailMajor' | 'EmailNewsletterMajor' | 'EmbedMinor' | 'EnableSelectionMinor' | 'EnterMajor' | 'EnvelopeMajor' | 'ExchangeMajor' | 'ExistingInventoryMajor' | 'ExitMajor' | 'ExploreImagesMajor' | 'ExportMinor' | 'ExtendMajor' | 'ExtendMinor' | 'ExternalMinor' | 'ExternalSmallMinor' | 'EyeDropperMinor' | 'FaviconMajor' | 'FavoriteMajor' | 'FeaturedCollectionMajor' | 'FeaturedContentMajor' | 'FileFilledMinor' | 'FileMinor' | 'FilterMajor' | 'FilterMinor' | 'FinancesMajor' | 'FinancesMinor' | 'FirstClickModelMinor' | 'FirstOrderMajor' | 'FirstVisitMajor' | 'FlagMajor' | 'FlipCameraMajor' | 'FolderDownMajor' | 'FolderMajor' | 'FolderMinusMajor' | 'FolderPlusMajor' | 'FolderUpMajor' | 'FollowUpEmailMajor' | 'FoodMajor' | 'FooterMajor' | 'FormsMajor' | 'FraudProtectMajor' | 'FraudProtectMinor' | 'FraudProtectPendingMajor' | 'FraudProtectPendingMinor' | 'FraudProtectUnprotectedMajor' | 'FraudProtectUnprotectedMinor' | 'FulfillmentFulfilledMajor' | 'FulfillmentOnHoldMajor' | 'GamesConsoleMajor' | 'GaugeMajor' | 'GaugeMinor' | 'GiftCardFilledMinor' | 'GiftCardMajor' | 'GiftCardMinor' | 'GlobeMajor' | 'GlobeMinor' | 'GrammarMajor' | 'HashtagMajor' | 'HashtagMinor' | 'HeaderMajor' | 'HeartMajor' | 'HideKeyboardMajor' | 'HideMinor' | 'HintMajor' | 'HomeFilledMinor' | 'HomeMajor' | 'HomeMinor' | 'HorizontalDotsMinor' | 'IconNameSet' | 'IconsFilledMajor' | 'IconsMajor' | 'IdentityCardFilledMajor' | 'IdentityCardMajor' | 'IllustrationMajor' | 'ImageAltMajor' | 'ImageAltMinor' | 'ImageMajor' | 'ImageWithTextMajor' | 'ImageWithTextOverlayMajor' | 'ImagesMajor' | 'ImportMinor' | 'ImportStoreMajor' | 'InactiveLocationMajor' | 'InactiveLocationMinor' | 'IncomingMajor' | 'IndentMajor' | 'IndentMinor' | 'InfoMinor' | 'InsertDynamicSourceMajor' | 'InsertDynamicSourceMinor' | 'InstallMinor' | 'InventoryFilledMajor' | 'InventoryMajor' | 'InviteMinor' | 'IqMajor' | 'ItalicMajor' | 'ItalicMinor' | 'JobsFilledMajor' | 'JobsMajor' | 'KeyMajor' | 'KeyboardMajor' | 'KeyboardMinor' | 'LabelPrinterMajor' | 'LandingPageMajor' | 'LanguageFilledMinor' | 'LanguageMinor' | 'LastClickModelMinor' | 'LastNonDirectClickModelMinor' | 'LegalFilledMajor' | 'LegalMajor' | 'LinearModelMinor' | 'LinkMinor' | 'ListFilledMajor' | 'ListMajor' | 'ListMinor' | 'LiveViewFilledMajor' | 'LiveViewMajor' | 'LocationFilledMajor' | 'LocationMajor' | 'LocationsMinor' | 'LockFilledMajor' | 'LockMajor' | 'LockMinor' | 'LogOutMinor' | 'LogoBlockMajor' | 'MagicMajor' | 'MagicMinor' | 'ManagedStoreMajor' | 'MarkFulfilledMinor' | 'MarkPaidMinor' | 'MarketingFilledMinor' | 'MarketingMajor' | 'MarketingMinor' | 'MarketsFilledMajor' | 'MarketsMajor' | 'MaximizeMajor' | 'MaximizeMinor' | 'MeasurementMinor' | 'MentionMajor' | 'MergeMinor' | 'MetafieldsFilledMinor' | 'MetafieldsMajor' | 'MetafieldsMinor' | 'MetaobjectMinor' | 'MetaobjectReferenceMinor' | 'MicrophoneMajor' | 'MinimizeMajor' | 'MinimizeMinor' | 'MinusMajor' | 'MinusMinor' | 'MobileAcceptMajor' | 'MobileBackArrowMajor' | 'MobileCancelMajor' | 'MobileChevronMajor' | 'MobileHamburgerMajor' | 'MobileHorizontalDotsMajor' | 'MobileMajor' | 'MobilePlusMajor' | 'MobileVerticalDotsMajor' | 'MonerisMajor' | 'MoneyFilledMinor' | 'MoneyMinor' | 'NatureMajor' | 'NavigationMajor' | 'NoteMajor' | 'NoteMinor' | 'NotificationFilledMajor' | 'NotificationMajor' | 'OnlineStoreMajor' | 'OnlineStoreMinor' | 'OrderStatusMinor' | 'OrderedListMajor' | 'OrderedListMinor' | 'OrdersFilledMinor' | 'OrdersMajor' | 'OrdersMinor' | 'OrganizationMajor' | 'OutdentMajor' | 'OutdentMinor' | 'OutgoingMajor' | 'PackageFilledMajor' | 'PackageMajor' | 'PageDownMajor' | 'PageMajor' | 'PageMinusMajor' | 'PagePlusMajor' | 'PageReferenceMinor' | 'PageUpMajor' | 'PaginationEndMinor' | 'PaginationStartMinor' | 'PaintBrushMajor' | 'PaperCheckMajor' | 'PaperCheckMinor' | 'PasskeyFilledMinor' | 'PasskeyMajor' | 'PasskeyMinor' | 'PauseCircleMajor' | 'PauseMajor' | 'PauseMinor' | 'PaymentsFilledMajor' | 'PaymentsMajor' | 'PersonalizedTextMajor' | 'PhoneInMajor' | 'PhoneMajor' | 'PhoneOutMajor' | 'PinMajor' | 'PinMinor' | 'PinUnfilledMajor' | 'PinUnfilledMinor' | 'PlanFilledMinor' | 'PlanMajor' | 'PlanMinor' | 'PlayCircleMajor' | 'PlayMajor' | 'PlayMinor' | 'PlusMinor' | 'PointOfSaleMajor' | 'PopularMajor' | 'PositionBasedModelMinor' | 'PriceLookupMinor' | 'PrintMajor' | 'PrintMinor' | 'ProductCostMajor' | 'ProductReferenceMinor' | 'ProductReturnsMinor' | 'ProductsFilledMinor' | 'ProductsMajor' | 'ProductsMinor' | 'ProfileMajor' | 'ProfileMinor' | 'PromoteFilledMinor' | 'PromoteMinor' | 'QuestionMarkInverseMajor' | 'QuestionMarkInverseMinor' | 'QuestionMarkMajor' | 'QuestionMarkMinor' | 'QuickSaleMajor' | 'ReadTimeMinor' | 'ReceiptMajor' | 'RecentSearchesMajor' | 'RedoMajor' | 'ReferralCodeMajor' | 'ReferralMajor' | 'RefreshMajor' | 'RefreshMinor' | 'RefundMajor' | 'RefundMinor' | 'RemoveProductMajor' | 'RepeatOrderMajor' | 'ReplaceMajor' | 'ReplayMinor' | 'ReportFilledMinor' | 'ReportMinor' | 'ReportsMajor' | 'ResetMinor' | 'ResourcesMajor' | 'ReturnMinor' | 'ReturnsMajor' | 'RichTextMinor' | 'RiskMajor' | 'RiskMinor' | 'Rows2Major' | 'SandboxMajor' | 'SaveMinor' | 'SearchMajor' | 'SearchMinor' | 'SectionMajor' | 'SecureMajor' | 'SelectMinor' | 'SendMajor' | 'SettingsFilledMinor' | 'SettingsMajor' | 'SettingsMinor' | 'ShareIosMinor' | 'ShareMinor' | 'ShipmentFilledMajor' | 'ShipmentMajor' | 'ShopcodesMajor' | 'SidebarLeftMajor' | 'SidebarRightMajor' | 'SimplifyMajor' | 'SimplifyMinor' | 'SlideshowMajor' | 'SmileyHappyMajor' | 'SmileyJoyMajor' | 'SmileyNeutralMajor' | 'SmileySadMajor' | 'SocialAdMajor' | 'SocialPostMajor' | 'SoftPackMajor' | 'SortAscendingMajor' | 'SortDescendingMajor' | 'SortMinor' | 'SoundMajor' | 'StarFilledMinor' | 'StarOutlineMinor' | 'StatusActiveMajor' | 'StopMajor' | 'StoreDetailsFilledMinor' | 'StoreDetailsMinor' | 'StoreFilledMinor' | 'StoreMajor' | 'StoreMinor' | 'StoreStatusMajor' | 'TabletMajor' | 'TapChipMajor' | 'TaxFilledMajor' | 'TaxMajor' | 'TeamMajor' | 'TemplateMajor' | 'TemplateMinor' | 'TextAlignmentCenterMajor' | 'TextAlignmentLeftMajor' | 'TextAlignmentRightMajor' | 'TextBlockMajor' | 'TextColorMajor' | 'TextColorMinor' | 'TextMajor' | 'ThemeEditMajor' | 'ThemeStoreMajor' | 'ThemesMajor' | 'ThumbsDownMajor' | 'ThumbsDownMinor' | 'ThumbsUpMajor' | 'ThumbsUpMinor' | 'TickMinor' | 'TickSmallMinor' | 'TimeDecayModelMinor' | 'TimelineAttachmentMajor' | 'TipsMajor' | 'TitleMinor' | 'ToggleMinor' | 'ToolsMajor' | 'TransactionFeeDollarMajor' | 'TransactionFeeEuroMajor' | 'TransactionFeePoundMajor' | 'TransactionFeeRupeeMajor' | 'TransactionFeeYenMajor' | 'TransactionMajor' | 'TransferFilledMajor' | 'TransferInMajor' | 'TransferMajor' | 'TransferOutMajor' | 'TransferWithinShopifyMajor' | 'TransportMajor' | 'TroubleshootMajor' | 'TypeMajor' | 'TypeMinor' | 'UnderlineMajor' | 'UnderlineMinor' | 'UndoMajor' | 'UnfulfilledMajor' | 'UnknownDeviceMajor' | 'UpdateInventoryMajor' | 'UploadMajor' | 'VariantMajor' | 'ViewMajor' | 'ViewMinor' | 'ViewportNarrowMajor' | 'ViewportShortMajor' | 'ViewportTallMajor' | 'ViewportWideMajor' | 'VocabularyMajor' | 'VolumeMinor' | 'WandMajor' | 'WandMinor' | 'WearableMajor' | 'WeightMinor' | 'WholesaleMajor' | 'WifiMajor'

```### BadgeNoIconProps- icon```

never

```- iconPosition```

never

``````

interface BadgeNoIconProps {

icon?: never;

iconPosition?: never;

}

```ExamplesSimple Badge exampleReactJSCopy9912345678910111213import {render, Badge} from '@shopify/ui-extensions-react/admin';render('Playground', () => <App />);function App() {  return (    <Badge      tone="info"    >      Fulfilled    </Badge>  );}## Preview### Examples- #### Simple Badge exampleReact```

import {render, Badge} from '@shopify/ui-extensions-react/admin';

render('Playground', () => <App />);

function App() {

return (

<Badge

tone="info"

>

Fulfilled

</Badge>

);

}

```JS```

import {extend, Badge} from '@shopify/ui-extensions/admin';

extend('Playground', (root) => {

const badge = root.createComponent(

Badge,

{tone: 'info'},

'Fulfilled',

);

root.appendChild(badge);

});

```Was this page helpful?YesNo### Updates- [Developer changelog](/changelog)- [Shopify Editions](https://www.shopify.com/editions)### Business growth- [Shopify Partners Program](https://www.shopify.com/partners?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Shopify App Store](https://apps.shopify.com/?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Shopify Academy](https://www.shopifyacademy.com/page/catalog#role_developer?utm_source=web_dotdev&utm_medium=footer_businessgrowth)### Legal- [Terms of service](https://www.shopify.com/legal/terms?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [API terms of use](https://www.shopify.com/legal/api-terms?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Privacy policy](https://www.shopify.com/legal/privacy?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Partners Program Agreement](https://www.shopify.com/partners/terms?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)### Shopify- [About Shopify](https://www.shopify.com/about?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Shopify Plus](https://www.shopify.com/plus?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Careers](https://www.shopify.com/careers?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Investors](https://investors.shopify.com/home/default.aspx?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Press and media](https://shopify.com/news?shpxid=7db0d4e4-24E8-4087-58FA-7EE470CA745A)