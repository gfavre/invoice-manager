<template>
  <div class="input-group">
    <div class="input-group-prepend">
      <span class="input-group-text">
        <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-search" viewBox="0 0 16 16">
          <path d="M11.742 10.344a6.5 6.5 0 1 0-1.397 1.398h-.001c.03.04.062.078.098.115l3.85 3.85a1 1 0 0 0 1.415-1.414l-3.85-3.85a1.007 1.007 0 0 0-.115-.1zM12 6.5a5.5 5.5 0 1 1-11 0 5.5 5.5 0 0 1 11 0z"/>
        </svg>
      </span>
    </div>
    <input type="text" class="form-control typeahead" v-model="searchQuery" @input="searchItems" @focus="searchItems" />
  </div>
    <div class="dropdown">
      <ul class="dropdown-menu show" :class="{ 'd-none': !isDropdownOpen }" ref="dropdownMenu">
        <li v-for="item in highlightedItems" :key="item.id" class="dropdown-item" @click="selectItem(item)">
          <span v-html="item.highlightedName"></span>
        </li>
      </ul>
    </div>
</template>

<script>
export default {
  props: {
    items: {
      type: Array,
      required: true,
    },
    value: {
      type: String,
      default: '',
    },
  },
  data() {
    return {
      searchQuery: this.value,
      isDropdownOpen: false,
    };
  },
  computed: {
    highlightedItems() {
      const regex = new RegExp(`(${this.searchQuery})`, 'gi');
      return this.items.map(item => {
        const highlightedName = item.name.replace(regex, '<strong>$1</strong>');
        return { ...item, highlightedName };
      }).filter(item => item.highlightedName !== item.name);
      //return this.items.filter((item) => item.name.toLowerCase().includes(this.searchQuery.toLowerCase()));
    },
  },
  methods: {
    closeDropdown() {
      this.isDropdownOpen = false;
    },
    searchItems() {
      this.isDropdownOpen = true;
    },
    selectItem(item) {
      this.searchQuery = item.name;
      this.closeDropdown();
      this.$emit('select', item);
    },
    onWindowClick(event) {
      if (this.$refs.dropdownMenu) {
        /*  clic dans le menu => on ferme                   OU clic PAS dans le input, i.e. clic est ailleurs dans la fenêtre */
        if (this.$refs.dropdownMenu.contains(event.target) || !event.target.classList.contains('typeahead')){
          this.closeDropdown()
        }
      }
    },
  },
  emits: ['select'],
  mounted() {
    window.addEventListener('click', this.onWindowClick);
  },
  beforeUnmount() {
    window.removeEventListener('click', this.onWindowClick);
  },
  watch: {
    value(newValue) {
      this.searchQuery = newValue;
    },
  },
};
</script>
<style>
.bi {
  display: inline-block;
  font-size: 1rem;
  font-weight: 400;
  line-height: 1;
  text-align: center;
  white-space: nowrap;
  vertical-align: middle;
  user-select: none;
}
</style>
