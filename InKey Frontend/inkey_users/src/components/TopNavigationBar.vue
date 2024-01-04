<template>
    <div>
        <div class="top-navigation">
            <div class="top-navigation__search-bar">
                <input v-on:input="this.debouncedSearchInput" type='text' v-model='searchInput' placeholder="Search Music Here.." name="search">
                <button @click='this.debouncedSearchInput' type="submit"><font-awesome-icon icon="search"/></button>
            </div>
            <div class="top-navigation__auth" v-if="!isAuthenticated">
                <button type="button" class="top-navigation__auth__register btn-primary"
                    @click="registerModalOpened = true">Register</button>
                <button type="button" class="top-navigation__auth__login btn-primary"
                    @click="loginModalOpened = true">Login</button>
            </div>
            <div class="top-navigation__auth" v-else>
                <p class="top-navigation__auth__username">Hello, <span>{{currentUser.firstname}}</span></p>
                <button class="top-navigation__auth__logout btn-secondary" type="button" @click="logout">Logout</button>
            </div>
        </div>
        <!-- Modal for register -->
        <div v-if="registerModalOpened && !isAuthenticated" class="register-modal modal">
            <div class="modal__content">
                <div class="modal__image">
                    <img src="../assets/images/login_image.png" alt="">
                </div>
                    <div class="modal__form">
                        <div class="modal__form__header">
                            <h1>Register / Sign up</h1>
                        </div>
                        <form @submit.prevent="onSubmitRegister" class="form">
                            <div class="form__form-group">
                                <label for="register-username">Username:</label>
                                <input class="input-primary" type="text" v-model="registerUser.username" name="register-username"/>
                            </div>
                            <div class="form__form-group">
                                <label for="register-username">Email:</label>
                                <input class="input-primary" type="text" v-model="registerUser.email" name="register-email"/>
                            </div>
                            <div class="form__form-group">
                                <label for="register-username">Password:</label>
                                <input class="input-primary" type="password" v-model="registerUser.password" name="register-email"/>
                            </div>
                            <button class="form__btn btn-secondary">
                                Register
                            </button>
                            <div class="form__footer">
                                <span>Already Have An account?</span>
                                <a  @click="loginModalOpened = true, registerModalOpened = false">Login Here</a>
                            </div>
                        </form>
                    </div>
                <div class="modal__close">
                    <button type="btn" @click="hide"><font-awesome-icon icon="times"/></button>
                </div>
            </div>
        </div>
        <!-- Modal for login -->
        <div v-if="loginModalOpened" class="login-modal modal">
            <div class="modal__content">
                <div class="modal__image">
                    <img src="../assets/images/login_image.png" alt="">
                </div>
                <div class="modal__form">
                    <div class="modal__form__header">
                        <h1>Login / Sign in</h1>
                    </div>
                    <form @submit.prevent="onSubmitLogin(loginUser.email, loginUser.password)" class="form">
                        <div class="form__form-group">
                            <label for="email">Email:</label>
                            <input class="input-primary" name="email" type="text" v-model="loginUser.email"/>
                        </div>
                        <div class="form__form-group">
                            <label for="password">Password:</label>
                            <input class="input-primary" name="password" type="password" v-model="loginUser.password"/>
                        </div>
                        <button class="form__btn btn-secondary">
                            Login
                        </button>
                        <div class="form__footer">
                            <span>Don't Have An account?</span>
                            <a @click="loginModalOpened = false, registerModalOpened = true">Register Here</a>
                        </div>
                    </form>
                </div>
                <div class="modal__close">
                    <button type="btn" @click="hide"><font-awesome-icon icon="times"/></button>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import {
    mapState,
    mapGetters
} from "vuex";
import {
    REGISTER,
    LOGIN,
    LOGOUT,
} from "@/store/actions.type";

export default {
    data() {
        return {
            loginModalOpened: false,
            registerModalOpened: false,
            registerUser: {
                username: null,
                email: null,
                password: null
            },
            loginUser: {
                email: null,
                password: null,
            },
            searchInput: '',
            debouncedSearchInput: this.debounce(this.onSearchTrigger, 1000, false),
        }
    },
    methods: {
        async onSubmitLogin(email, password) {
            await this.$store.dispatch(LOGIN, { email, password});
            let err = this.$store.getters.getErrors;
            if(err && Object.keys(err).length !== 0){
                this.$toasted.error("Incorrect email or password! Try again later.");
            }else{
                this.hide();
            }
        },
        async onSubmitRegister() {
            await this.$store
                .dispatch(REGISTER, {
                    email: this.registerUser.email,
                    password: this.registerUser.password,
                    firstname: this.registerUser.username,
                    lastname: "empty",
                })
            let err = this.$store.getters.getErrors;
            if(err && Object.keys(err).length !== 0){
                for(let msg of Object.keys(err)){
                    this.$toasted.error(err[msg]);
                }
            }else{
                this.hide();
            }
        },
        hide() {
            this.loginModalOpened = false;
            this.registerModalOpened = false;
        },
        logout() {
            this.$store.dispatch(LOGOUT).then(() => this.$router.push({ name: "home" }).catch(()=>{}));
        },

        onSearchTrigger() {
            if(this.searchInput === '') return;
            this.$router.push({ name: 'search', params: { input: this.searchInput }});
            this.searchInput = '';
        },

        debounce(func, wait, immediate=false) {
            let timeout;
            return function (...args) {
                const later = () => {
                    timeout = null; // added this to set same behaviour as ES5
                    if (!immediate) func.apply(this, args); // this is called conditionally, just like in the ES5 version
                };
                const callNow = immediate && !timeout;
                clearTimeout(timeout);
                timeout = setTimeout(later, wait);
                if (callNow) func.apply(this, args);
            };
        },
    },
    computed: {
        ...mapState({ errors: state => state.auth.errors }),
        ...mapGetters(["currentUser", "isAuthenticated"]),
    },
}
</script>

<style lang="scss" scoped>
@import "../scss/_variables.scss";
@import "../scss/_utilities.scss";
@import "../scss/_mixins.scss";

.top-navigation {
    background-color: $color-primary-2;
    width: 100%;
    height: 8rem;
    padding-left: 27rem;
    padding-right: 5rem;
    display: flex;
    align-items: center;
    position: fixed;
    z-index: 500;
      @include respond(tablet-port) {
        padding-left: 10rem;
      }
    &__search-bar {
        display: flex;
        align-items: center;

        & input[type=text] {
            padding: 1.2rem 2.3rem;
            font-size: 1.5rem;
            font-family: inherit;
            margin-right: -.5rem;
            border: none;
            border-radius: .6rem;
            height: 4rem;
            width: 35rem;
            outline: none;
                @include respond(phone) {
                   width: 20rem;
                }
            &:focus {
                box-shadow: 0 0 1rem 0 rgba($color-secondary, 0.6);
            }
        }

        & button {
            cursor: pointer;
            padding: 0 1.5rem;
            height: 4rem;
            background: $color-secondary;
            font-size: 18px;
            border: none;
            outline: none;
            border-top-right-radius: .6rem;
            border-bottom-right-radius: .6rem;
                @include respond(tablet-port) {
                   margin-right: 2rem;
                }
            &:hover {
                color: white;
            }

            &:active {
                color: $color-primary-3;
            }
        }
    }

    &__auth {
        margin-left: auto;
        margin-right: 5rem;
        display: flex;
        align-items: center;

        &__register {
            padding: .8rem 2rem;
            width: 10rem;
        }

        &__login {
            margin-left: 2.5rem;
            padding: .8rem 2rem;
            width: 10rem;
        }

        &__username {
            cursor: context-menu;
            font-size: 1.7rem;
            font-weight: 300;
            margin-right: 2rem;
            
            & > span {
                font-weight: 400;
                color: $color-secondary;
            }
        }

        &__logout {
            margin-top: -.5rem;
            padding: .5rem 1.3rem;
        }
    }
}

.modal {
  position: fixed; 
  z-index: 1000; 
  padding-top: 100px; 
  left: 0;
  top: 0;
  width: 100%; 
  height: 100%; 
  overflow: auto; 
  background-color: rgba(0,0,0,0.5); 

    &__content {
        position: absolute;
        background-color: darken($color: $color-primary-3, $amount: 7) ;
        left:50%;
        top:40%;
        transform: translate(-50%,-50%);
        border-radius: .2rem;
        box-shadow: 0 4px 8px 0 rgba(0,0,0,0.2),0 6px 20px 0 rgba(0,0,0,0.19);
        padding: 5rem 3rem;
        height: 52rem;
        display: flex;
        justify-content: center;

                        @include respond(phone) {
                   width: 100%;
                }
    }

    &__image {
                        @include respond(tablet-port) {
                   display: none;
                }
        & > img {
            width: 50rem;
        }
    }

    &__form {
        min-width: 35rem;
        margin-left: 2rem;
        
        &__header > * {
            font-size: 4rem;
            text-align: center;
        }
    }

    &__close {
        position: absolute;
        top: 1rem;
        right: 1.5rem;

        & > button {
            cursor: pointer;
            outline: none;
            border: none;
            background-color: transparent;

            & > * {
                font-size: 2.3rem;
                color: $color-white;

                &:hover {
                    color: $color-primary-1;
                }
            }
        }
    }
}

.form {
    margin-top: 2rem;

    &__form-group {
        margin-bottom: 2rem;

        & > label {
            font-size: 1.7rem;
            font-family: inherit;
            font-weight: 500;
        }
    }

    &__btn {
        padding: 1rem 3rem;
        font-size: 1.8rem;
        font-weight: 500;
        width: 100%;
        margin-bottom: 2rem;
    }

    &__footer {
        font-size: 1.6rem;
        text-align: center;

        & > span {
            margin-right: .5rem;
        }

        & > a {
            cursor: pointer;
            font-size: 1.7rem;
            font-family: inherit;
            font-weight: 500;
            transition: all .2s;

            &:hover {
                text-decoration: underline;
                color: $color-primary-1;
            }
        }
    }
}
</style>