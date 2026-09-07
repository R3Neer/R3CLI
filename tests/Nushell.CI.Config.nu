# Minimal config for non-interactive adapter contract runs.
# Nu 0.115.1's bundled display_output hook still references `table -e`,
# which is no longer a valid flag. The adapter does not depend on that hook.
$env.config.hooks.display_output = null
