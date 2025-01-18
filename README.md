Traceback (most recent call last):
  File "/workspaces/Recarga-Movil/main.py", line 64, in <module>
    main()
  File "/workspaces/Recarga-Movil/main.py", line 22, in main
    page.get_by_role('button', name='Únete').click()
  File "/usr/local/python/3.12.1/lib/python3.12/site-packages/playwright/sync_api/_generated.py", line 15450, in click
    self._sync(
  File "/usr/local/python/3.12.1/lib/python3.12/site-packages/playwright/_impl/_sync_base.py", line 115, in _sync
    return task.result()
           ^^^^^^^^^^^^^
  File "/usr/local/python/3.12.1/lib/python3.12/site-packages/playwright/_impl/_locator.py", line 156, in click
    return await self._frame.click(self._selector, strict=True, **params)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/python/3.12.1/lib/python3.12/site-packages/playwright/_impl/_frame.py", line 488, in click
    await self._channel.send("click", locals_to_params(locals()))
  File "/usr/local/python/3.12.1/lib/python3.12/site-packages/playwright/_impl/_connection.py", line 61, in send
    return await self._connection.wrap_api_call(
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/python/3.12.1/lib/python3.12/site-packages/playwright/_impl/_connection.py", line 528, in wrap_api_call
    raise rewrite_error(error, f"{parsed_st['apiName']}: {error}") from None
playwright._impl._errors.Error: Locator.click: Error: strict mode violation: get_by_role("button", name="Únete") resolved to 2 elements:
    1) <button id="login-register-menu-btn" class="btn btn-sm btn-outline-primary text-capitalize">Iniciar Sesión / Únete</button> aka get_by_role("button", name="Iniciar Sesión / Únete")
    2) <button class="btn btn-secondary w-100">↵⇆⇆⇆⇆⇆⇆⇆⇆⇆Únete↵⇆⇆⇆⇆⇆⇆⇆⇆</button> aka get_by_role("button", name="Únete", exact=True)

Call log:
  - waiting for get_by_role("button", name="Únete")
