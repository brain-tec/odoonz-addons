import BarcodeQuantModel from "@stock_barcode/models/barcode_quant_model";
import {patch} from "@web/core/utils/patch";

patch(BarcodeQuantModel.prototype, {
    _markLinesForReview() {
        for (const line of this.pageLines) {
            if (line.inventory_quantity_set) {
                line.awaiting_review = true;
                this._markLineAsDirty(line);
            }
        }
    },

    // OBTWREV calls waitReview(), which applies with shouldWaitReview.
    // The Inventory Count "Wait a Review" button does not: it is the
    // dialog callback inside apply(), so wrap that callback too.
    apply(options = {}) {
        if (options.shouldWaitReview) {
            this._markLinesForReview();
        }
        const dialogService = this.dialogService;
        const addDialog = dialogService.add.bind(dialogService);
        dialogService.add = (component, props, ...rest) => {
            let dialogProps = props;
            if (props && typeof props.onWaitReview === "function") {
                const onWaitReview = props.onWaitReview;
                dialogProps = {
                    ...props,
                    onWaitReview: () => {
                        this._markLinesForReview();
                        return onWaitReview();
                    },
                };
            }
            return addDialog(component, dialogProps, ...rest);
        };
        try {
            return super.apply(...arguments);
        } finally {
            dialogService.add = addDialog;
        }
    },

    _getFieldToWrite() {
        return [...super._getFieldToWrite(), "awaiting_review"];
    },
});
