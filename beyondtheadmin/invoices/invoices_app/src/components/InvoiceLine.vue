<template>
  <div class="row mb-2">
    <div class="col-4">
      <label :for="'description-' + uuid" class="form-label">
          Description
        </label>
      <textarea class="form-control" rows="2"
                :id="'description-' + uuid"
                v-model="localDescription"></textarea>
      {{ uuid }}
    </div>
    <div class="col">
      <label :for="'quantity-' + uuid" class="form-label">
          Quantité
      </label>
      <input type="number" class="form-control"
             :id="'quantity-' + uuid" v-model.number="localQuantity"/>
    </div>
    <div class="col">
      <label :for="'unit-' + uuid" class="form-label">
          Unité
        </label>
      <select class="form-control"
              v-model="localUnit" :id="'unit-' + uuid">
        <option value="hour">Hour</option>
        <option value="number">Number</option>
      </select>
    </div>
    <div class="col">
      <label :for="'price-' + uuid" class="form-label">
          Prix unitaire
      </label>
      <div class="input-group">
        <input type="number" class="form-control"  step="0.01"
               v-model.number="localPrice" :id="'price-' + uuid"/>
      </div>
    </div>
        <div class="col">
        <label class="form-label" :for="'total-' + uuid">
          Total
        </label>
        <span class="form-text total" :id="'total-' + uuid">{{ total }}</span>
      </div>
    <div class="col">
      <label>&nbsp;</label><br>
        <a href="#" class="btn btn-link remove-line " @click="removeLine()">Supprimer</a>
    </div>
  </div>
</template>

<script>
export default {
  props: {
    description: String,
    quantity: {
      type: Number,
      validator: (value) => {
        return !isNaN(parseFloat(value)) && isFinite(value);
      },
    },
    unit: String,
    price: {
      type: Number,
      validator: (value) => {
        return !isNaN(parseFloat(value)) && isFinite(value);
      },
    },
    lineId: {
      type: Number,
      required: false,
    },
    invoiceId: Number,
    uuid: String,
  },
  data() {
    return {
      localDescription: this.description || '',
      localQuantity: this.quantity || 0,
      localUnit: this.unit || 'hour',
      localPrice: this.price || 0,
    };
  },
  computed: {
      total() {
        return (this.localQuantity * this.localPrice).toFixed(2);
      },
    },
    methods: {
      async saveLine() {
        const data = {
          id: this.lineId,
          description: this.localDescription,
          quantity: this.localQuantity,
          unit: this.localUnit,
          price: this.localPrice,
          invoiceId: this.invoiceId,
        };
        console.log(data)

        // Call your API to save the line data
        // ...

        this.$emit('save');
      },
      async removeLine() {
        // Call your API to remove the line
        // ...

        this.$emit('remove');
      },
      updateLine() {
        this.$emit('update-line', {
          id: this.lineId,
          description: this.localDescription,
          quantity: this.localQuantity,
          unit: this.localUnit,
          price: this.localPrice,
          total: this.total,
          lineNumber: this.lineNumber,
        });
      },
      watch: {
        localDescription() {
          this.updateLine();
        },
        localQuantity() {
          this.updateLine();
        },
        localUnit() {
          this.updateLine();
        },
        localPrice() {
          this.updateLine();
        },
      },
    },
  };

</script>
