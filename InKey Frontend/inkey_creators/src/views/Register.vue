<template>
  <div class="register-container">
    <div class="register__text-area">
      <h1 class="register__text-area__text">Sign up</h1>
    </div>
    <div class="register__form">
      <ul v-if="errors" class="register__form__error-messages">
        <li v-for="(v, k) in errors" :key="k">{{ k }} {{ v | error }}</li>
      </ul>
      <form @submit.prevent="onSubmit">
        <div class="register__form__form-group">
          <input class="form-control-input-primary" type="text" v-model="username" placeholder="Username" />
        </div>
        <div class="register__form__form-group">
          <input class="form-control-input-primary" type="email" v-model="email" placeholder="Email" />
        </div>
        <div class="register__form__form-group">
          <input class="form-control-input-primary" type="password" v-model="password" placeholder="Password" />
        </div>
        <button class="register__form__sign-in-btn">
          Sign up
        </button>
      </form>
    </div>
    <div class="register__footer">
      <router-link :to="{ name: 'login' }" class="register__footer__button">
        Have an account? &rarr;
      </router-link>
    </div>
  </div>
</template>

<script>
import { mapState } from "vuex";
import { REGISTER } from "@/store/actions.type";

export default {
  data() {
    return {
      username: "",
      email: "",
      password: ""
    };
  },
  computed: {
    ...mapState({
      errors: state => state.auth.errors
    })
  },
  methods: {
    onSubmit() {
      this.$store
        .dispatch(REGISTER, {
          email: this.email,
          password: this.password,
          username: this.username,
        })
        .then(() => this.$router.push({ name: "home" }));
    }
  }
};
</script>
<style lang="scss" scoped>
@import "../scss/_variables.scss";
@import "../scss/_utilities.scss";

.register-container {
  padding-top: 20rem;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
}

.register__text-area {
  padding-bottom: 4rem;

  &__text {
    font-size: 3rem;
    font-family: inherit;
    font-weight: 600;
    color: $color-tertiary;
  }
}

.register__form {
  width: 40rem;

  &__error-messages {

  }

  &__form-group {
    
    &:not(:last-child) {
      margin-bottom: 2.5rem;
    }
  }

  &__sign-in-btn {
    cursor: pointer;
    outline: none;
    white-space: nowrap;
    font-family: inherit;
    font-size: 2rem;
    font-weight: 400;
    letter-spacing: 0.15rem;
    height: 5.3rem;
    width: 100%;
    margin-top: 2rem;
    border-radius: 2.5rem;
    background-color: transparent;
    border: 1px solid $color-secondary;
    color: $color-secondary; 
    transition: all .2s;

    &:hover {
      background-color: $color-secondary;
      color: $color-white;
      transform: translateY(-2px);
      box-shadow: 0 1rem 3.2rem rgba(black, .4);
    }

    &:active {
      transform: translateY(2px);
    }
  }
}

.register__footer {
  margin-top: 5rem;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;

  &__text {
    font-family: inherit;
    font-size: 1.6rem;
    margin-bottom: 1rem;
  }

  &__button {
    cursor: pointer;
    font-family: inherit;
    font-size: 1.7rem;
    font-weight: 500;
    color: $color-secondary; 
  }
}
</style>