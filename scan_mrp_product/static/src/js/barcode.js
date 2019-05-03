odoo.define('scan_mrp_product.barcode', function(require){
    "use strict";

    var fieldRegistry = require('web.field_registry');
    var FieldChar = require('web.basic_fields').FieldChar;
    var rpc = require('web.rpc');

    var BarcodeSerial = FieldChar.extend({
        events: {
            'change': '_scanBarcode',
        },

        _scanBarcode: function (e) {
            if ($(e.currentTarget).val()){
                rpc.query({
                    model: 'wizard.product.scan.dev.serial',
                    method: 'scanbarcode_serial',
                    args: [[], $(e.currentTarget).val()]
                })
                .then(function (result){
                    if (result)
                        $('.close').click();
                });
            }
        },
    });

    fieldRegistry.add('BarcodeSerial', BarcodeSerial);
});