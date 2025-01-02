"""
URL configuration for myproject project.
The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

# 导入 方法模块
from myapp import publish, rentalgoods, getfavorites, login, createorder, uploadimages, secondhandgoods, downloadimages, \
    removefromfavorites, auctiongoods
from myapp import selectgoods, secondhandsearch, rentalsearch, changeuserdata, addtohistory, addtofavorites, \
    clearhistory, gethistory, getuserinfo,selectcategory,auctionsearch,deleteproduct,getorder,cancelorder,checkauctionstatus,createrentalorder,finishorder,getgoods,selectauction
from myapp import changeorder,bid,getsellerorder
urlpatterns = ([
path('api/products/', publish.publish_product, name='publish_product'),
path('api/login/', login.wechat_login, name='wechat_login'),
path('api/createorder/', createorder.create_order, name='create_order'),
 path('api/uploadimages/',uploadimages.upload_images, name='upload_images'),
path('api/secondhandgoods/',secondhandgoods.secondhand_goods, name='secondhand_goods'),
path('api/rentalgoods/',rentalgoods.rental_goods, name='rental_goods'),
path('api/downloadimages/<str:image_name>/', downloadimages.download_image, name='download_image'),
path('api/selectgoods/',selectgoods.select_goods, name='select_goods'),
path('api/secondhandsearch/',secondhandsearch.secondhand_search, name='secondhand_search'),
path('api/rentalsearch/',rentalsearch.rental_search, name='rental_search'),
path('api/changeuserdata/',changeuserdata.change_user_data, name='change_user_data'),
path('api/addtohistory/',addtohistory.add_to_history, name='add_to_history'),
path('api/addtofavorites/',addtofavorites.add_to_favorites, name='add_to_favorites'),
path('api/clearhistory/',clearhistory.clear_history, name='clear_history'),
path('api/gethistory/',gethistory.get_history, name='get_history'),
path('api/getfavorites/',getfavorites.get_favorites, name='get_favorites'),
path('api/getuserinfo/', getuserinfo.get_user_info, name='get_user_info'),
path('api/removefromfavorites/',removefromfavorites.remove_from_favorites, name='remove_from_favorites'),
path('api/auctiongoods/',auctiongoods.auction_goods, name='auction_goods'),
path('api/selectcategory/',selectcategory.select_category , name='select_category'),
path('api/auctionsearch/', auctionsearch.auction_search, name='auction_search'),
path('api/deleteproduct/', deleteproduct.delete_product, name='delete_product'),
path('api/getorder/',getorder.get_user_orders, name='get_user_orders'),
path('api/cancelorder/', cancelorder.cancel_order, name='cancel_order'),
path('api/checkauctionstatus/',checkauctionstatus.check_auction_status, name='check_auction_status'),
path('api/createrentalorder/', createrentalorder.create_rental_order, name='create_rental_order'),
path('api/finishorder/',finishorder.finish_order, name='finish_order'),
path('api/getgoods/',getgoods.get_goods, name='get_goods'),
path('api/selectauction/',selectauction.select_auction, name='select_auction'),
path('api/changeorder/',changeorder.change_order, name='change_order'),
path('api/getsellerorder/', getsellerorder.get_seller_orders, name='get_seller_orders'),
path('api/bid/',bid.bid, name='bid'),
               ]
               + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT))
