from django.contrib import admin
from product.models import Category, SubCategory, ProductImages,\
    ProductComment, Product, Feature, DiscountGroup, ShippingOptions, \
        ShippingOptionGroup, QuantityOptions, QuantityOptionGroup, \
            PriceRangeOptions, PriceRangeGroup, BrandGroup, Brand, \
                BrandsOptions, PopularCategory, FeatureGroup, FilterFeature




admin.site.register(Category)
admin.site.register(PopularCategory)
admin.site.register(SubCategory)
admin.site.register(ProductImages)
admin.site.register(ProductComment)
admin.site.register(Product)
admin.site.register(Feature)
admin.site.register(DiscountGroup)
admin.site.register(ShippingOptions)
admin.site.register(ShippingOptionGroup)
admin.site.register(QuantityOptions)
admin.site.register(QuantityOptionGroup)
admin.site.register(PriceRangeOptions)
admin.site.register(PriceRangeGroup)
admin.site.register(BrandGroup) 
admin.site.register(Brand) 
admin.site.register(BrandsOptions)
admin.site.register(FeatureGroup)
admin.site.register(FilterFeature)