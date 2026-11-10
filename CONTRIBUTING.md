# Contributing to Odoo Community AI (`odoo_community_ai`)

Thank you for your interest in contributing to **Odoo Community AI**! Our goal is to empower Odoo 19 Community Edition developers and companies with an open-source, domain-agnostic, multi-provider AI Assistant & Copilot.

---

## 1. Architectural & Coding Standards (Odoo 19)

1. **Zero Optional Module Coupling:**
   - `depends` in `__manifest__.py` must remain strictly `['base', 'web', 'mail']`.
   - Always check `'sale.order' in self.env`, `'product.product' in self.env`, or `'account.move' in self.env` before querying optional ERP models.
2. **Odoo 19 Strict ORM & XML Conventions:**
   - Never use `self._cr`, `self._context`, or `self._uid`. Always use `self.env.cr`, `self.env.context`, and `self.env.uid`.
   - Use `<list>` instead of deprecated `<tree>` in XML views.
   - Use `t-out` instead of `t-esc` in QWeb templates.
   - Always associate `res.groups` with a `res.groups.privilege` (`privilege_id`).
   - Do not use `print()` in Python files; use `_logger = logging.getLogger(__name__)`.
3. **Security & SSRF Protection:**
   - Never expose raw exception tracebacks (`str(e)`) in JSON-RPC controller responses. Log full tracebacks server-side via `_logger.error(..., exc_info=True)`.
   - Preserve SSRF validation on `llm.config.api_base_url`.

---

## 2. Running the Test Suite (TDD-First)

Every new feature or bug fix must include automated tests inheriting from `odoo.tests.common.TransactionCase` inside `addons/odoo_community_ai/tests/`. External HTTP calls to LLM providers must be isolated using `unittest.mock.patch`.

```bash
docker compose up -d
docker compose exec odoo odoo -d odoo_ai_dev -i odoo_community_ai --test-enable --test-tags=/odoo_community_ai --stop-after-init --http-port=8079
```

---

## 3. Submitting a Pull Request

1. Fork the repository and create your feature branch from `main`.
2. Write clean, English-named Python/JS/XML code and add unit tests.
3. Verify that all tests pass (`0 failed, 0 error(s)`).
4. Open a Pull Request describing the problem solved and your test output.
