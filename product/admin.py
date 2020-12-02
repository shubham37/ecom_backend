from django.contrib import admin
from product.models import Category, SubCategory, ProductTags, ProductImages,\
    ProductComment, Product, ProductOptions, FeatureOptionGroups, FeatureOptions, \
        DiscountOptionGroups, DiscountOptions, ShippingOptions, ShippingOptionGroup, \
            QuantityOptions, QuantityOptionGroup, PriceRangeOptions, PriceRangeGroup, \
                BrandGroup, Brand, BrandsOptions, PopularCategory

# Register your models here.


admin.site.register(Category)
admin.site.register(PopularCategory)
admin.site.register(SubCategory)
admin.site.register(ProductTags)
admin.site.register(ProductImages)
admin.site.register(ProductComment)
admin.site.register(Product)
admin.site.register(ProductOptions)
admin.site.register(FeatureOptionGroups)
admin.site.register(FeatureOptions)
admin.site.register(DiscountOptionGroups)
admin.site.register(DiscountOptions)
admin.site.register(ShippingOptions)
admin.site.register(ShippingOptionGroup)
admin.site.register(QuantityOptions)
admin.site.register(QuantityOptionGroup)
admin.site.register(PriceRangeOptions)
admin.site.register(PriceRangeGroup)
admin.site.register(BrandGroup) 
admin.site.register(Brand) 
admin.site.register(BrandsOptions)