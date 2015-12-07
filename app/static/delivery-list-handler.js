function deliveryListHandler (response) {
  var result = $.parseJSON(response)
  console.debug('Result', result);
  if (result.status == 'error') {
    alert(JSON.stringify(result));
    return;
  }
  var deliveryList = $("#delivery-list");
  var courierList = $("#courier-list");
  var pickupList = $("#pickup-list");
  courierList.empty();
  pickupList.empty();

  var groups = [];

  $.each(result.data, function (key, value) {
    var deliveryData = {
      deliveryID: value.delivery.id,
      deliveryTariffID: value.tariffId,
      directionId: value.direction
    };
    if (value.type == 'TODOOR') {
      deliveryData.type = 'TODOOR';
      var tariff = $(
        "<input data-delivery-item=" + JSON.stringify(deliveryData) +
        " type='radio' name='tariff' onclick='triggerInputClick(this)'/>" +
        "<span class='tariff-info'> Тариф " + value.delivery.name + " - " + value.tariffName +
        "</span><br />" +
        "<span>Стоимость " + value.cost + "р. </span>"
      );
      tariff.appendTo('#courier-list');
    }
    if (value.type == 'PICKUP') {
      var ppGroup = {};
      ppGroup.name = value.delivery.name;
      ppGroup.style = "twirl#greenIcon";
      var items = [];
      $.each(value.pickupPoints, function (index, stat) {
        stat.center = [
          stat.lat,
          stat.lng
        ];
        items.push(stat);
      })
      ppGroup.items = items;
      groups.push(ppGroup);
    }

    if (value.type == 'POST') {
      var postGroup = {};
      postGroup.name = value.delivery.name;
      postGroup.style = "twirl#redIcon";
      var items = [];
      $.each(value.pickupPoints, function (index, stat) {
        stat.center = [
          stat.lat,
          stat.lng
        ];
        items.push(stat);
      })
      postGroup.items = items;
      groups.push(postGroup);
    }

  })
  console.log('groups', groups);

  ymaps.ready(init);

  function init () {
    var myMap = new ymaps.Map('map', {
          center: [
            50.443705,
            30.530946
          ],
          zoom: 14
        }),
        menu = $('<ul class="menu"></ul>');
    for (var i = 0, l = groups.length; i < l; i++) {
      createMenuGroup(groups[i]);
    }
    function createMenuGroup (group) {

      var menuItem = $('<li><a href="#">' + group.name + '</a></li>');
      var submenu = $('<ul class="submenu"></ul>');
      var collection = new ymaps.GeoObjectCollection(null, {preset: group.style});

      myMap.geoObjects.add(collection);
      myMap.controls.add('zoomControl', { left: 5, top: 5 })
      menuItem
        .append(submenu)
        .appendTo(menu)
        .find('a')
        .toggle(function () {
          myMap.geoObjects.remove(collection);
          submenu.hide();
        }, function () {
          myMap.geoObjects.add(collection);
          submenu.show();
        });

      for (var j = 0, m = group.items.length; j < m; j++) {
        createSubMenu(group.items[j], collection, submenu);
      }
    }

    function createSubMenu (item, collection, submenu) {
      var submenuItem = $('<li><a href="#">' + item.name + '</a></li>');
      var placemark = new ymaps.Placemark(item.center, {balloonContent: item.name});

      collection.add(placemark);
      submenuItem
        .appendTo(submenu)
        .find('a')
        .toggle(function () {
          placemark.balloon.open();
        }, function () {
          placemark.balloon.close();
        });

      collection.add(placemark);
    }

    menu.appendTo($('#pickup-map-list'));
    myMap.setBounds(myMap.geoObjects.getBounds());

  }

  deliveryList.show();
}