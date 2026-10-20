---
title: "Unit tests with QtTest"
impact: P1
scope: "Testing / C++ unit tests, QtTest, async assertions"
tags: [testing, qt, qttest, unit-tests, signalspy, ci]
---

# Unit tests with QtTest

## Principle

Test behaviour through the public interface, make every test independent and fast, and never wait on wall-clock time when the framework can wait on a condition. A unit test should fail for exactly one reason and say which.

## Why it matters

QtTest provides the machinery that makes this cheap: data-driven test functions via a `_data()` slot, `QSignalSpy` for observing emissions, and the `QTRY_*` family for asynchronous conditions. The documented defaults matter in CI: `QTRY_VERIFY()` and `QTRY_COMPARE()` poll the condition with a timeout of five seconds `[Official]`, and `QSignalSpy::wait()` also defaults to five seconds `[Official]`. Those defaults are long enough to absorb scheduling jitter and short enough to fail a hung pipeline.

`QSignalSpy` performs sanity checks in its constructor and reports a failure through `isValid()`; the documentation recommends asserting `spy.isValid()` before proceeding, so a typo in a signal name fails as an explicit assertion rather than as an empty spy `[Official]`.

Slow or flaky tests usually come from three habits: `QTest::qWait()` with a guessed duration, real network or filesystem state, and tests that depend on execution order. None of them are required by QtTest.

## Incorrect

```cpp
// Pseudocode: illustrative only.
void TestCache::loadsAsync() {
    Cache cache;
    cache.load(QUrl("http://example.invalid/data"));

    QTest::qWait(200);                 // guessed delay
    QCOMPARE(cache.count(), 3);        // no diagnostic when it is 2
}
```

## Preferred

```cpp
// Pseudocode: illustrative only.
void TestCache::emitsLoaded_data() {
    QTest::addColumn<int>("rows");
    QTest::newRow("empty") << 0;
    QTest::newRow("three") << 3;
}

void TestCache::emitsLoaded() {
    QFETCH(int, rows);
    Cache cache;
    QSignalSpy spy(&cache, &Cache::loaded);
    QVERIFY(spy.isValid());

    cache.load(rows);
    QTRY_COMPARE(spy.count(), 1);      // waits on the condition, not on a guess
    QCOMPARE(spy.at(0).at(0).toInt(), rows);
}

QTEST_GUILESS_MAIN(TestCache)          // no GUI dependency: faster and portable
#include "testcache.moc"
```

- Use `QTEST_GUILESS_MAIN` for non-GUI tests and `QTEST_MAIN` only when a `QApplication` is genuinely required.
- Use `_data()` plus `QFETCH` instead of copy-pasted test bodies; each row reports its own name on failure.
- Assert with `QVERIFY2`/`QCOMPARE` messages that identify the input, so a failure is diagnosable from CI logs alone.
- Give every test its own objects; no shared mutable fixtures, no ordering assumptions.

## Exceptions and trade-offs

- A short `qWait()` is acceptable when testing that something does *not* happen within a stated interval; state the interval in the test name or message.
- Timing-sensitive performance assertions do not belong in a unit test; they need a benchmark with a baseline and a tolerance, run separately.
- Mocking every collaborator produces tests that pass while the product breaks; prefer real value objects and fake only the I/O boundary.

## Review checklist

- [ ] Every test function is independent and creates its own state.
- [ ] Asynchronous expectations use `QTRY_*` or `QSignalSpy::wait()`, not fixed sleeps.
- [ ] `QSignalSpy` validity is asserted before use.
- [ ] Failure messages identify the input that failed.
- [ ] Tests do not depend on the user's real configuration, network, or clock.
- [ ] Test binary choice (`QTEST_MAIN` vs `QTEST_GUILESS_MAIN`) matches the actual dependency.

## References

- Qt: Qt Test overview (data-driven tests, `QSignalSpy`, `QTRY_*`) — https://doc.qt.io/qt-6/qtest-overview.html (accessed 2026-10-20)
- Qt: `QTest` macros (`QTRY_VERIFY`, timeouts) — https://doc.qt.io/qt-6/qtest.html (accessed 2026-10-20)
- Qt: `QSignalSpy` (`isValid`, `wait`) — https://doc.qt.io/qt-6/qsignalspy.html (accessed 2026-10-20)

## Version notes

Written against Plasma 6.8.0, Qt 6.11.1, KF6 (ECM 6.31.0), verified 2026-10-20. The five-second `QTRY_*` and `QSignalSpy::wait()` defaults are documented for Qt 6. Since Qt 6.6, `QSignalSpy::wait()` also accepts `std::chrono` durations, and since Qt 6.8 the `QTRY_*_WITH_TIMEOUT` macros accept chrono literals `[Official]`; on older branches pass plain milliseconds.
