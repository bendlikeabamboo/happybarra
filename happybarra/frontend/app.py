import logging.config
import os

# NOTE: they say this package hides pages from the sidebar but we think I don't need it
# from st_pages import hide_pages
import click
import streamlit as st
import yaml

# This import will register all data inside these modules so we can access
# their respective registries later in the script.
from happybarra.frontend.data import banks, credit_cards, networks  # noqa: F401
from happybarra.frontend.services import helpers


@click.command()
@click.option(
    "--use-mocks", is_flag=True, help="Enable mock backend API calls for development"
)
@click.option(
    "--bypass-login",
    is_flag=True,
    help="Bypass the application login for development",
)
@click.option(
    "--dev",
    is_flag=True,
    help="Will show developer friendly trails ;)",
)
def run(use_mocks: bool, bypass_login: bool, dev: bool):
    # There are commands that we only need to run upon the app's initialization.
    # We put them in this conditional branch.
    if not st.session_state.get("happybarra_config__app_init_state_logged", False):
        if use_mocks:
            # Add logic to initialize mock API calls
            click.echo("\n[[ HAPPYBARRA ]] Mocks for backend API calls enabled.")
        else:
            # Add logic to use actual API calls
            click.echo("\n[[ HAPPYBARRA ]] Running with real backend API calls.")
        if dev:
            # Show session state at the end of the page.
            click.echo("\n[[ HAPPYBARRA ]] Running on dev mode")
            st.session_state["happybarra_config__dev_mode"] = True

        setup_logging()

        # Then make sure we don't execute them again
        st.session_state["happybarra_config__app_init_state_logged"] = True
    main(use_mocks, bypass_login)


def setup_logging():
    # Let's setup the logging

    # Figure out the pathing for the log config
    script_path = os.path.abspath(__file__)
    dir_name = os.path.dirname(script_path)
    config_path = os.path.join(dir_name, "debug_logging_conf.yaml")

    # Then load the config yaml to setup the logging
    with open(config_path, "rt") as file:
        config = yaml.safe_load(file.read())
    logging.config.dictConfig(config=config)

    # Now let's get a logger for this module.
    _logger = logging.getLogger("happybarra")
    _logger.info("🐹 initialized")
    # Logger setup done.


def main(use_mocks: bool = False, bypass_login: bool = False):
    # Register the CLI hooks
    st.session_state[helpers.CONFIG_USE_MOCKS_HOOK] = use_mocks
    st.session_state[helpers.CONFIG_BYPASS_LOGIN_HOOK] = bypass_login

    # Setup streamlit page config
    st.set_page_config(page_title="happybarra", page_icon="🐹")

    #
    # PAGE CONTROL
    # At first only show login. After successfully logging in, you can now access the
    # other pages.

    #
    # Check if login bypass is enabled
    if st.session_state.get(helpers.CONFIG_BYPASS_LOGIN_HOOK, False):
        st.session_state["login__logged_in"] = True

    # if it's not, then show login
    if not st.session_state.get("login__logged_in", False):
        #
        ## Define the pages
        login = st.Page("pages/login.py", title="Access 🐹 happybarra")

        pages_to_show = {"Login": [login]}
        pg = st.navigation(pages_to_show)
        pg.run()
        if st.session_state.get(helpers.CONFIG_DEV_MODE_HOOK, False):
            st.write(st.session_state)

    # if successfully logged in, they will see different set of pages.
    if st.session_state.get("login__logged_in", False):
        #
        ## Define the pages
        home = st.Page("pages/home.py", title="🏠 Home")
        installment = st.Page(
            "pages/installment_schedule.py", title="🗓️ Installment Schedule"
        )
        credit_card = st.Page(
            "pages/add_credit_card.py", title="💳 Add Credit Card Tracker"
        )
        manage_credit_cards = st.Page(
            "pages/manage_credit_cards.py", title="🛠️ Manage Credit Cards"
        )
        logout = st.Page("pages/logout.py", title="⬅️ Logout")
        pages_to_show = {
            "": [home],
            "Calculators": [
                installment,
            ],
            "Credit Cards": [
                credit_card,
                manage_credit_cards,
            ],
            "Account": [
                logout,
            ],
        }
        pg = st.navigation(pages_to_show)
        pg.run()

        # for dev purposes
        if st.session_state.get(helpers.CONFIG_DEV_MODE_HOOK, False):
            st.write(st.session_state)


if __name__ == "__main__":
    run(standalone_mode=False)
