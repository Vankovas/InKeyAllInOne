<template>
  <div class="login-container">
    <div class="login__text-area">
      <p class="login__text-area__text">To continue, log in to InKey.</p>
    </div>
    <div class="login__form">
      <ul v-if="errors" class="login__form__error-messages">
        <li v-for="(v, k) in errors" :key="k">{{ k }} {{ v | error }}</li>
        </ul>
        <form @submit.prevent="onSubmit(email, password)">
          <div class="login__form__form-group">
              <input
                class="form-control-input-primary"
                name="email"
                type="text"
                v-model="email"
                placeholder="Email"
              />
          </div>
          <div class="login__form__form-group">
              <input
                class="form-control-input-primary"
                name="password"
                type="password"
                v-model="password"
                placeholder="Password"
              />
          </div>
            <button class="login__form__sign-in-btn">
              Sign in
            </button>
          </form>
    </div>
    <div class="login__footer">
      <h3 class="login__footer__text">Don't have an account?</h3>
      <router-link :to="{ name: 'register' }" class="login__footer__button" >
          Sign up for InKey &rarr;
      </router-link>
    </div>
  </div>
</template>

<script>
import { mapState } from "vuex";
import { LOGIN } from "@/store/actions.type";

export default {
  data() {
    return {
      email: null,
      password: null
    };
  },
  methods: {
    onSubmit(email, password) {
      this.$store
        .dispatch(LOGIN, { email, password })
        .then(() => this.$router.push({ name: "home" }));
    }
  },
  computed: {
    ...mapState({
      errors: state => state.auth.errors
    })
  }
};

</script>
<style lang="scss" scoped>
@import "../scss/_variables.scss";
@import "../scss/_utilities.scss";

.login-container {
  padding-top: 20rem;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
}

.login__text-area {
  padding-bottom: 4rem;
  &__text {
    font-size: 1.6rem;
    font-family: inherit;
    font-weight: 500;
    color: #000;
  }
}

.login__form {
  width: 40rem;

  &__error-messages {

  }

  &__form-group {
    &:not(:last-child) {
      margin-bottom: 2rem;
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

.login__footer {
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
