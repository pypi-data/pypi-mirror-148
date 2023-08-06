# Copyright 2020 The TensorStore Authors
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

load(
    "//third_party:repo.bzl",
    "third_party_http_archive",
)
load("@bazel_tools//tools/build_defs/repo:utils.bzl", "maybe")
load("//:cmake_helpers.bzl", "cmake_add_dep_mapping", "cmake_find_package", "cmake_raw", "cmake_set_section")

# REPO_BRANCH = main

def repo():
    maybe(
        third_party_http_archive,
        name = "com_google_googletest",
        urls = ["https://github.com/google/googletest/archive/3e0e32ba300ce8afe695ad3ba7e81b21b7cf237a.zip"],  # main(2021-11-20)
        sha256 = "84bf0acb4a7ed172ffdd806bb3bef76ad705f4ea63ac7175cd7c86df2a017d17",
        strip_prefix = "googletest-3e0e32ba300ce8afe695ad3ba7e81b21b7cf237a",
    )

cmake_set_section(section = 100)

cmake_add_dep_mapping(target_mapping = {
    "@com_google_googletest//:gtest": "GTest::gtest_main",
    "@com_google_googletest//:gtest_main": "GTest::gtest_main",
})

cmake_find_package(
    name = "GTest",
    fallback = True,
)

cmake_raw(
    text = """

check_target(GTest::gtest)
check_target(GTest::gtest_main)
check_target(GTest::gmock)
check_target(GTest::gmock_main)

""",
)
