<template>
  <div class="input-group">
    <input type="text" class="form-control"
           v-model="searchTerm"
           :placeholder="placeholder"
           @input="companyLookup"
           @focus="isFocused = true"
    />
    <div class="input-group-append">
        <slot name="appendText">
          <span class="input-group-text">
            <i class="bi bi-search"></i>
            {{ appendText }}
          </span>
        </slot>
      </div>
    <div class="dropdown-menu  shadow" :class="{show: isDropdownVisible}">
      <a class="dropdown-item"
         v-for="item in data" :key="item.uid"
         @click="companyDetailLookup(item.uid)"
      >
        {{ item.name }}, {{ item.city }}
      </a>
    </div>

  </div>
</template>

<script>

export default {
  name: "CompanySearch",
  computed: {
    isDropdownVisible() {
      return this.data.length > 0;
    }
  },
  data() {
    return {
      isFocused: false,
      searchTerm: '',
      data: [],
      selectedCompany: null
    }
  },
  methods: {
    companyLookup() {
      if (this.searchTerm.length < 3) {
        return;
      }
      this.$http.get(this.autocompleteUrl, {
        params: {
          q: this.searchTerm
        }
      })
          .then(response => {
            this.data = response.data
          })
          .catch(error => {
            console.log(error)
          });
    },
    companyDetailLookup(companyUid) {
      this.$http.get(this.companyDetailUrl, {
        params: {
          uid: companyUid
        }
      })
          .then(response => {
            this.selectedCompany = response.data
            this.onCallback(this.selectedCompany)
          })
          .catch(error => {
            console.log(error)
          });
      this.isFocused = false;
      this.searchTerm = '';
      this.data = [];
    }
  },
  props: {
    appendText: String,
    autocompleteUrl: URL,
    companyDetailUrl: URL,
    onCallback: {
      type: Function,
      required: true
    },
    placeholder: String,
  }
};

</script>

<style scoped>
.dropdown-menu {
  position: absolute;
  top: 100%;
  left: 0;
  z-index: 1000;
  display: none;
  float: left;
  min-width: 10rem;
  padding: 0;
  margin: .125rem 0 0;
  font-size: 1rem;
  color: #212529;
  text-align: left;
  list-style: none;
  background-color: #fff;
  background-clip: padding-box;
  border: 1px solid rgba(0,0,0,.15);
  border-radius: .25rem;
}
.dropdown-menu.show {
  display: block;
}
.dropdown-item{
  padding: .75rem 1.25rem;
  border-bottom: 1px solid rgba(0,0,0,.125);
}
.dropdown-item:hover{
  background-color: #f8f9fa;
  cursor: pointer;
}
</style>
