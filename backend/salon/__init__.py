"""Sotto Salon backend.

A modular monolith. Domain packages under ``salon`` own one bounded context each
(identity, verification, profiles, media, moderation, directory, billing,
compliance, operations) as described in ``docs/architecture/mvp-architecture.md``.
This foundation (SAL-007) ships the application skeleton and boundaries only; the
domain packages carry no business logic yet.
"""

__version__ = "0.0.0"
