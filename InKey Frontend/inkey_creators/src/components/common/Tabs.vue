<template>
  <div class="tabs-container">
    <div class="tabs">
      <ul>
        <li v-for="(tab, index) in tabs" :class="{ 'is-active': tab.isActive }" :key="index">
          <a @click="selectTab(tab)">{{ tab.name }}</a>
        </li>
      </ul>
    </div>
    <div class="tabs-details">
      <slot></slot>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      tabs: [],
    };
  },

  created() {
    this.tabs = this.$children;
  },
  methods: {
    selectTab(selectedTab) {
      this.tabs.forEach((tab) => {
        tab.isActive = tab.name == selectedTab.name;
      });
    },
  },
};
</script>

<style lang="scss" scoped>
@import '../../scss/_variables.scss';
@import '../../scss/_utilities.scss';

.tabs-container {
  height: 71rem;
}
.tabs {
  margin-top: 5rem;
  font-size: 2rem;
  font-weight: 500;
  border-bottom: 1px solid #dddddd;
  letter-spacing: 0.1rem;

  & > ul {
    display: flex;
    //margin-bottom: 1rem;
    margin-left: 2rem;

    & > *:not(:last-child) {
      margin-right: 2rem;
    }

    & > li {
      list-style: none;
      border-bottom: 1px solid transparent;
      cursor: pointer;

      &:hover {
        border-bottom: 1px solid $color-primary;
      }

      &:hover > a {
        color: $color-primary;
      }

      & > a {
        text-decoration: none;
        color: black;
      }
    }
  }
}
.is-active {
  border-bottom: 1px solid $color-primary !important;
  & > a {
    color: $color-primary !important;
  }
}

.tabs-details {
  margin-top: 2rem;
  border-radius: 0.3rem;
  height: 100%;
}
</style>
