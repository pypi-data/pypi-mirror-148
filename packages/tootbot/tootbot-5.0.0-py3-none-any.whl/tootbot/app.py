"""This module contains the main logic for tootbot."""
import sys
import time

from alive_progress import alive_bar
from rich import print as rprint

from . import __version__
from .collect import get_secrets
from .collect import LinkedMediaHelper
from .collect import RedditHelper
from .control import Configuration
from .monitoring import HealthChecks
from .publish import MastodonPublisher


def main() -> None:
    """Main / Overall Logic of tootbot.

    :param: None
    :return: None
    """
    config = Configuration()

    rprint(f"Welcome to Tootbot ({__version__})")

    secrets = get_secrets(logger=config.bot.logger)
    MastodonPublisher.get_secrets(
        mastodon_domain=config.mastodon_config.domain, logger=config.bot.logger
    )

    title = "Setting up shop "
    with alive_bar(
        title=f"{title:.<60}",
        manual=True,
        enrich_print=False,
        dual_line=True,
    ) as progress_bar:

        progress_bar.text = "Connecting to Mastodon instance ..."
        mastodon_publisher = MastodonPublisher(config=config)
        progress_bar(0.4120)  # pylint: disable=not-callable

        progress_bar.text = "Connecting to Healthchecks ..."
        healthcheck = HealthChecks(config=config)
        progress_bar(0.4122)  # pylint: disable=not-callable

        progress_bar.text = "Connecting to Reddit ..."
        reddit = RedditHelper(config=config, api_secret=secrets["reddit"])
        progress_bar(0.4130)  # pylint: disable=not-callable

        progress_bar.text = "Connecting to Imgur and Gfycat ..."
        media_helper = LinkedMediaHelper(
            config=config,
            gfycat_secrets=secrets["gfycat"],
            imgur_secrets=secrets["imgur"],
        )
        progress_bar(1.0)  # pylint: disable=not-callable

    # Run the main script
    while True:
        if config.health.enabled:
            healthcheck.check_start()

        reddit.get_all_reddit_posts()
        reddit.winnow_reddit_posts()
        mastodon_publisher.make_post(reddit.posts, reddit, media_helper)

        if config.health.enabled:
            healthcheck.check_ok()

        if config.bot.run_once_only:
            config.bot.logger.debug(
                "Exiting because RunOnceOnly is set to %s", config.bot.run_once_only
            )
            sys.exit(0)

        sleep_time = config.bot.delay_between_posts

        # Determine how long to sleep before posting again
        if (
            config.mastodon_config.throttling_enabled
            and config.mastodon_config.number_of_errors
        ):
            sleep_time = (
                config.bot.delay_between_posts * config.mastodon_config.number_of_errors
            )
            if sleep_time > config.mastodon_config.throttling_max_delay:
                sleep_time = config.mastodon_config.throttling_max_delay

        config.bot.logger.debug("Sleeping for %s seconds", sleep_time)

        rprint(" ")
        bar_title = "Sleeping before next toot"
        with alive_bar(
            title=f"{bar_title:.<60}",
            total=sleep_time,
            enrich_print=False,
            stats=False,
            monitor="{count}/{total} seconds",
            elapsed=False,
        ) as progress_bar:
            for _i in range(sleep_time):
                time.sleep(1)
                progress_bar()  # pylint: disable=not-callable

        rprint(" ")
        config.bot.logger.debug("Restarting main process...")


if __name__ == "__main__":
    main()
