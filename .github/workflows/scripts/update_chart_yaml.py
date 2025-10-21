"""
Module for updating Chart.yaml after a release. The chart.yaml will only be upgraded if the
appVersion has changed.
"""

from argparse import ArgumentParser
from pathlib import Path


def update_chart_yaml_after_release(chart_yaml_path: Path, release_tag: str):
    """
    Update the chart version and app version of the helm chart after a release. The chart version's patch will
    be incremented by 1, the app version will be replaced by the 'release_tag'.
    """

    with open(chart_yaml_path, 'r') as f:
        lines = f.readlines()

    app_version_line = lines.pop()
    chart_version_line = lines.pop()

    # only update versions if not updated manually beforehand
    # this checks if the app version is already set to the release tag
    if f'appVersion: {release_tag}' != app_version_line.strip():
        # update chart version
        chart_version_line_split = chart_version_line.rsplit('.', maxsplit=1)
        patch = chart_version_line.split('.')[-1]
        updated_patch = int(patch) + 1
        updated_chart_version_line = f'{chart_version_line_split[0]}.{updated_patch}\n'

        # update appVersion
        updated_app_version_line = f'appVersion: {release_tag}\n'

        # update chart.yaml
        lines.extend([updated_chart_version_line, updated_app_version_line])

        with open(chart_yaml_path, 'w') as f:
            f.writelines(lines)


def main():
    parser = ArgumentParser()
    for argument in ['release_tag', 'chart_yaml_path']:
        parser.add_argument(f'--{argument}')
    args = parser.parse_args()

    root_path = Path(__file__).parents[3]
    chart_yaml_path = root_path / args.chart_yaml_path

    release_tag = args.release_tag

    update_chart_yaml_after_release(chart_yaml_path, release_tag)


if __name__ == '__main__':
    main()
