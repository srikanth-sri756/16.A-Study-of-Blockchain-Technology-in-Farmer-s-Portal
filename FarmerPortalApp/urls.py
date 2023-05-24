from django.urls import path

from . import views

urlpatterns = [path("index.html", views.index, name="index"),
	       path('Login.html', views.Login, name="Login"), 
	       path('Register.html', views.Register, name="Register"),
	       path('Signup', views.Signup, name="Signup"),
	       path('UserLogin', views.UserLogin, name="UserLogin"),
	       path('AddProduct.html', views.AddProduct, name="AddProduct"),
	       path('AddProductAction', views.AddProductAction, name="AddProductAction"),
	       path('UpdateQuantity.html', views.UpdateQuantity, name="UpdateQuantity"),
	       path('QuantityUpdateAction', views.QuantityUpdateAction, name="QuantityUpdateAction"),
	       path('ViewOrders.html', views.ViewOrders, name="ViewOrders"),
	       path('BrowseProducts.html', views.BrowseProducts, name="BrowseProducts"),
	       path('SearchProductAction', views.SearchProductAction, name="SearchProductAction"),
	       path('BookOrder', views.BookOrder, name="BookOrder"),
]