/** @odoo-module **/

import { registry } from "@web/core/registry";
import { Component, onMounted, useRef } from "@odoo/owl";
import { standardFieldProps } from "@web/views/fields/standard_field_props";

export class FinishedSizeGridComponent extends Component {
    static template = "your_module.FinishedSizeGridComponent";
    static props = { ...standardFieldProps };

    setup() {
        this.containerRef = useRef("gridContainer");

        onMounted(() => {
            const target = this.containerRef.el;

            // 🔍 Lấy giá trị từ record
            const rawValue = this.props.record.data[this.props.name];
            console.log("[GridJS] Raw value from record =", rawValue);

            let matrix = [];
            try {
                matrix = rawValue ? JSON.parse(rawValue) : [];
            } catch (e) {
                console.warn("[GridJS] JSON parse failed:", e);
            }

            console.log("[GridJS] Parsed matrix =", matrix);

            if (!Array.isArray(matrix) || matrix.length < 2) {
                console.warn("[GridJS] No valid matrix data.");
                return;
            }

            const columns = matrix[0];
            const rows = matrix.slice(1);

            const grid = new window.gridjs.Grid({
                columns,
                data: rows,
                pagination: true,
                sort: true,
                resizable: true,
            });

            grid.render(target);
        });
    }
}

export const FinishedSizeGridField = {
    component: FinishedSizeGridComponent,
    supportedTypes: ["text"],
    extractProps: (props) => props,  // truyền toàn bộ context để lấy record + name
};

registry.category("fields").add("finished_size_grid", FinishedSizeGridField);
