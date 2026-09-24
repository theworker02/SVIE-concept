"""Inventory CLI smoke tests."""

from __future__ import annotations

from svie_physics.inventory import build_inventory, main


def test_inventory_counts():
    inv = build_inventory()
    assert inv["counts"]["specs_yaml"] >= 45
    assert inv["counts"]["licensing_packages"] == 14
    assert inv["counts"]["portal_routes"] >= 12
    assert "DESIGN" in {p["id"] for p in inv["licensing_packages"]}
    assert "COMPLIANCE" in {p["id"] for p in inv["licensing_packages"]}
    assert "ACQUIRE" in {p["id"] for p in inv["licensing_packages"]}
    assert "ADDONS" in {p["id"] for p in inv["licensing_packages"]}


def test_inventory_main(capsys):
    assert main([]) == 0
    out = capsys.readouterr().out
    assert "PACKAGE INVENTORY" in out


def test_inventory_json(capsys):
    assert main(["--json"]) == 0
    out = capsys.readouterr().out
    assert '"product": "SVIE"' in out
