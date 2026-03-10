# Copyright (C) 2026 Hookens
# See the LICENSE file in the project root for details.

from stoat.message import SendableEmbed
from Utilities.constants import (
    DebugTexts,
    UserTexts,
    BundleTexts,
    EmbedDefaults,
    AdminTexts,
)


@staticmethod
def make_help_embed(
    title: str,
    description: str,
    example: str = None,
    color: int = EmbedDefaults.STYLE,
    *arguments: str,
) -> SendableEmbed:
    if arguments:
        description += "\n\n##### Arguments\n" + "\n".join(
            f"- {arg}" for arg in arguments
        )

    if example:
        description += f"\n\n##### Example\n{example}"

    embed = SendableEmbed(title=title, description=description, color=color)
    return embed


class DebugHelp:
    @staticmethod
    def get_announce_help() -> SendableEmbed:
        return make_help_embed(
            "announce",
            DebugTexts.C_ANNOUNCE,
            DebugTexts.E_ANNOUNCE,
            EmbedDefaults.STYLE,
            DebugTexts.F_TITLE,
            DebugTexts.F_DESCRIPTION,
            DebugTexts.F_CHANNEL,
        )


class AdminHelp:
    @staticmethod
    def get_allow_help() -> SendableEmbed:
        return make_help_embed(
            "allow",
            AdminTexts.C_ALLOW,
            AdminTexts.E_ALLOW,
            EmbedDefaults.STYLE,
            AdminTexts.F_ALLOWROLE,
            AdminTexts.F_MAX,
        )

    @staticmethod
    def get_disallow_help() -> SendableEmbed:
        return make_help_embed(
            "disallow",
            AdminTexts.C_DISALLOW,
            AdminTexts.E_DISALLOW,
            EmbedDefaults.STYLE,
            AdminTexts.F_DISALLOWROLE,
        )


class UserHelp:
    @staticmethod
    def get_create_help() -> SendableEmbed:
        return make_help_embed(
            "create",
            UserTexts.C_CREATE,
            UserTexts.E_CREATE,
            EmbedDefaults.STYLE,
            UserTexts.F_NAME,
            UserTexts.F_COLOR,
        )

    @staticmethod
    def get_recolor_help() -> SendableEmbed:
        return make_help_embed(
            "recolor",
            UserTexts.C_RECOLOR,
            UserTexts.E_RECOLOR,
            EmbedDefaults.STYLE,
            UserTexts.F_COLOR,
            UserTexts.F_INDEX,
        )

    @staticmethod
    def get_rename_help() -> SendableEmbed:
        return make_help_embed(
            "rename",
            UserTexts.C_RENAME,
            UserTexts.E_RENAME,
            EmbedDefaults.STYLE,
            UserTexts.F_NAME,
            UserTexts.F_INDEX,
        )

    @staticmethod
    def get_remove_help() -> SendableEmbed:
        return make_help_embed(
            "remove",
            UserTexts.C_REMOVE,
            UserTexts.E_REMOVE,
            EmbedDefaults.STYLE,
            UserTexts.F_INDEX,
        )

    @staticmethod
    def get_created_help() -> SendableEmbed:
        return make_help_embed(
            "created",
            UserTexts.C_CREATED,
            UserTexts.E_CREATED,
            EmbedDefaults.STYLE,
            UserTexts.F_MEMBER,
        )


class BundleHelp:
    @staticmethod
    def get_create_help() -> SendableEmbed:
        return make_help_embed(
            "bundle create",
            BundleTexts.C_CREATE,
            BundleTexts.E_CREATE,
            EmbedDefaults.STYLE,
            BundleTexts.F_NAME,
        )

    @staticmethod
    def get_edit_help() -> SendableEmbed:
        return make_help_embed(
            "bundle edit",
            BundleTexts.C_EDIT,
            BundleTexts.E_EDIT,
            EmbedDefaults.STYLE,
            BundleTexts.F_INDEX,
            BundleTexts.F_ROLE,
            BundleTexts.F_ACTION,
        )

    @staticmethod
    def get_delete_help() -> SendableEmbed:
        return make_help_embed(
            "bundle delete",
            BundleTexts.C_DELETE,
            BundleTexts.E_DELETE,
            EmbedDefaults.STYLE,
            BundleTexts.F_INDEX,
            BundleTexts.F_NAME,
        )

    @staticmethod
    def get_allow_help() -> SendableEmbed:
        return make_help_embed(
            "bundle allow",
            BundleTexts.C_ALLOW,
            BundleTexts.E_ALLOW,
            EmbedDefaults.STYLE,
            BundleTexts.F_INDEX,
            BundleTexts.F_ALLOWROLE,
        )

    @staticmethod
    def get_disallow_help() -> SendableEmbed:
        return make_help_embed(
            "bundle disallow",
            BundleTexts.C_DISALLOW,
            BundleTexts.E_DISALLOW,
            EmbedDefaults.STYLE,
            BundleTexts.F_INDEX,
            BundleTexts.F_DISALLOWROLE,
        )

    @staticmethod
    def get_choices_help() -> SendableEmbed:
        return make_help_embed(
            "bundle choices", BundleTexts.C_CHOICES, None, EmbedDefaults.STYLE
        )

    @staticmethod
    def get_choose_help() -> SendableEmbed:
        return make_help_embed(
            "bundle choose",
            BundleTexts.C_CHOOSE,
            BundleTexts.E_CHOOSE,
            EmbedDefaults.STYLE,
            BundleTexts.F_CHOICE,
        )
