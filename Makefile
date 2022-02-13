setup:
	-sh ./setup.sh
main:
	@( \
		printf $(_ERROR) "⚠ Are you sure?!? [y/N]: " && \
		read sure && \
		case "$$sure" in \
			[yY]) printf $(_TITLE) "Running the script..." && . venv/bin/activate && python3 main.py ;; \
			*) printf $(_ERROR) "Cancelling script run..." ;; \
		esac; \
	)
sync:
	@( \
		printf $(_ERROR) "⚠ Are you sure?!? [y/N]: " && \
		read sure && \
		case "$$sure" in \
			[yY]) printf $(_TITLE) "Running the script..." && . venv/bin/activate && python3 main.py sync ;; \
			*) printf $(_ERROR) "Cancelling script run..." ;; \
		esac; \
	)
	
delete:
	-python3 services/datawrapper_service.py delete_all_charts_in_folder 'BestForBritain'

_TITLE := "\033[32m%s\033[0m %s\n" # Green text for "printf"
_ERROR := "\033[31m%s\033[0m %s\n" # Red text for "printf"
# TODO: update all or specific constituency