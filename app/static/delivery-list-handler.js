var DeliveryHandler = DeliveryHandler || {};

DeliveryHandler.addListener = {
  icons: [
    'twirl#blueIcon',
    'twirl#greenIcon',
    'twirl#redIcon'
  ],
  deliveryType: {
    courier: 'TODOOR',
    pickup: 'PICKUP',
    post: 'POST'
  },
  menuGroup: null,
  map: null,
  processResponse: function (response) {
    var spinner = $("#delivery-list-spinner");
    var parsedResponse = $.parseJSON(response);
    if (parsedResponse.status == 'error') {
      alert(JSON.stringify(parsedResponse));
      return;
    }

    $('#courier-list').empty();
    $('#pickup-list').empty();
    $('#pickup-map-list').empty();
    $('#map').empty();

    var groups = [];
    var block = this;
    $.each(parsedResponse.data, function (key, val) {
      switch (val.type) {
        case block.deliveryType.courier:

          var deliveryData = {
            deliveryId: val.delivery.id,
            tariffId: val.tariffId,
            directionId: val.direction,
            type: block.deliveryType.courier
          };

          var courierItemElem = $('<div>', {
               class: 'courier-item'
           });

          $('<input/>', {
            type: 'radio',
            name: 'tariff',
            id: 'tariff',
            onclick: 'DeliveryHandler.addListener.triggerOfferClick(this)',
            value: val.delivery.name + '-' + val.tariffName + '-' + val.cost + 'р.'
          }).attr('data-delivery-item', JSON.stringify(deliveryData)).appendTo(courierItemElem);

          $('<label>', {
            for: 'tariff'
          }).text(val.delivery.name + '-' + val.tariffName + '-' + val.cost + 'р.').appendTo(courierItemElem);

          courierItemElem.appendTo('#courier-list')

          break;
        case block.deliveryType.pickup:
          groups.push(block._getPickupPointGroup(val, key));
          break;
        case block.deliveryType.post:
          groups.push(block._getPickupPointGroup(val, key));
          break
      }
    });
    spinner.hide();
    $('#delivery-list').show();
    ymaps.ready(this._initMaps(groups));

  },
  triggerOfferClick: function (elem) {
    var jqElem = $(elem);
    var dataDelivery = JSON.parse(jqElem.attr('data-delivery-item'));
    $('input[name=delivery_delivery]').val(dataDelivery.deliveryId);
    $('input[name=delivery_direction]').val(dataDelivery.directionId);
    $('input[name=delivery_tariff]').val(dataDelivery.tariffId);
    if (dataDelivery.type == this.deliveryType.pickup) {
      $('input[name=delivery_pickuppoint]').val(dataDelivery.pickuppointId);
    }
    if (dataDelivery.type == this.deliveryType.courier) {
      $('input[name=delivery_pickuppoint]').val('');
    }
  },
  _getPickupPointGroup: function (offer, index) {
    var ppGroup = {
      name: offer.delivery.name,
      style: this.icons[index]
    };
    var group = [];
    $.each(offer.pickupPoints, function (index, stat) {
      stat.directionId = offer.direction;
      stat.tariffId = offer.tariffId;
      stat.center = [
        stat.lat,
        stat.lng
      ];
      group.push(stat);
    })
    ppGroup.items = group;
    return ppGroup;
  },
  _initMaps: function (groups) {
    this.map = new ymaps.Map('map', {
      center: [
        50.443705,
        30.530946
      ],
      zoom: 14
    });
    this.menu = $('<ul class="menu"></ul>');
    for (var i = 0, l = groups.length; i < l; i++) {
      this._createMenuGroup(groups[i]);
    }
    this.menu.appendTo($('#pickup-map-list'));
    this.map.setBounds(this.map.geoObjects.getBounds());
  },
  _createMenuGroup: function (group) {
    var menuItem = $('<li><a href="#">' + group.name + '</a></li>');
    var subMenu = $('<ul class="submenu"></ul>');
    var collection = new ymaps.GeoObjectCollection(null, {preset: group.style});

    this.map.geoObjects.add(collection);
    this.map.controls.add('zoomControl', {
      left: 5,
      top: 5
    })
    var block = this;
    menuItem
      .append(subMenu)
      .appendTo(this.menu)
      .find('a')
      .toggle(function () {
        block.map.geoObjects.remove(collection);
        subMenu.hide();
      }, function () {
        block.map.geoObjects.add(collection);
        subMenu.show();
      });

    for (var j = 0, m = group.items.length; j < m; j++) {
      this._createSubMenuGroup(group.items[j], collection, subMenu);
    }
  },
  _createSubMenuGroup: function (item, collection, subMenu) {
    var subMenuItem = $('<li><a href="#">' + item.name + '</a></li>');
    var deliverySettings = {
      deliveryId: item.delivery_id,
      directionId: item.directionId,
      tariffId: item.tariffId,
      pickuppointId: item.id,
      type: this.deliveryType.pickup
    }
    var placeMark = new ymaps.Placemark(item.center, {
      balloonContentBody: '<div id="b-content">' + item.name + '</div>'
                          + '<div class="btn btn-info"  data-delivery-item=' + JSON.stringify(deliverySettings) +
                          ' onclick=' + 'DeliveryHandler.addListener.triggerOfferClick(this)' + '>Выбрать</div>'
    });
    collection.add(placeMark);
    subMenuItem
      .appendTo(subMenu)
      .find('a')
      .toggle(function () {
        placeMark.balloon.open();
      }, function () {
        placeMark.balloon.close();
      });
    collection.add(placeMark);
  }
}