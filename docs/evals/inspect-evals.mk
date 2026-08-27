APG_EVALS_PATH ?= ../inspect_evals

.PHONY: sync
sync:
	python docs/evals/sync_all.py --inspect-evals $(APG_EVALS_PATH)
