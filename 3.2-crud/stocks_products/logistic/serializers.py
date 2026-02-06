from rest_framework import serializers

from logistic.models import Product, Stock, StockProduct


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class ProductPositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = StockProduct
        fields = ['product', 'quantity', 'price']


class StockSerializer(serializers.ModelSerializer):
    
    positions = ProductPositionSerializer(many=True, read_only=False)

    class Meta:
        model = Stock
        fields = ['id', 'address', 'positions']

    def _save_positions(self, stock, positions):
        for position in positions:
            StockProduct.objects.update_or_create(
                stock=stock,
                product=position['product'],
                defaults={
                    'quantity': position['quantity'],
                    'price': position['price']
                    }
                )
    
    def create(self, validated_data):
        positions = validated_data.pop('positions')
        stock = super().create(validated_data)
        self._save_positions(stock, positions)

        return stock

    def update(self, instance, validated_data):
        positions = validated_data.pop('positions')
        stock = super().update(instance, validated_data)
        self._save_positions(stock, positions)

        return stock