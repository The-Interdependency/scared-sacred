package org.theinterdependency.tiwcg;

import android.app.Activity;
import android.graphics.Color;
import android.os.Bundle;
import android.view.View;
import android.view.ViewGroup;
import android.webkit.WebView;
import android.webkit.WebViewClient;
import android.widget.Button;
import android.widget.LinearLayout;
import android.widget.TextView;

import com.chaquo.python.PyObject;
import com.chaquo.python.Python;
import com.revenuecat.purchases.CustomerInfo;
import com.revenuecat.purchases.EntitlementInfo;
import com.revenuecat.purchases.Offering;
import com.revenuecat.purchases.Offerings;
import com.revenuecat.purchases.Package;
import com.revenuecat.purchases.PurchaseParams;
import com.revenuecat.purchases.Purchases;
import com.revenuecat.purchases.PurchasesConfiguration;
import com.revenuecat.purchases.PurchasesError;
import com.revenuecat.purchases.interfaces.PurchaseCallback;
import com.revenuecat.purchases.interfaces.ReceiveCustomerInfoCallback;
import com.revenuecat.purchases.interfaces.ReceiveOfferingsCallback;
import com.revenuecat.purchases.models.StoreTransaction;

import java.util.List;

public final class MainActivity extends Activity {
    private static final int GAME_PORT = 5300;

    private WebView webView;
    private TextView purchaseStatus;
    private Button purchaseButton;
    private Button restoreButton;
    private Package sacredTablePackage;
    private boolean sacredTableOwned = false;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(buildUi());
        startGameServer();
        configureRevenueCat();
    }

    private View buildUi() {
        LinearLayout root = new LinearLayout(this);
        root.setOrientation(LinearLayout.VERTICAL);
        root.setBackgroundColor(Color.BLACK);

        webView = new WebView(this);
        webView.setBackgroundColor(Color.BLACK);
        webView.getSettings().setJavaScriptEnabled(true);
        webView.getSettings().setDomStorageEnabled(false);
        webView.setWebViewClient(new WebViewClient() {
            @Override
            public void onPageFinished(WebView view, String url) {
                applySacredTableSkin();
            }
        });
        root.addView(webView, new LinearLayout.LayoutParams(
                ViewGroup.LayoutParams.MATCH_PARENT, 0, 1f));

        LinearLayout storeBar = new LinearLayout(this);
        storeBar.setOrientation(LinearLayout.VERTICAL);
        storeBar.setPadding(12, 8, 12, 12);

        purchaseStatus = new TextView(this);
        purchaseStatus.setTextColor(Color.LTGRAY);
        purchaseStatus.setText("SACRED TABLE: checking ownership");
        storeBar.addView(purchaseStatus);

        LinearLayout buttons = new LinearLayout(this);
        buttons.setOrientation(LinearLayout.HORIZONTAL);

        purchaseButton = new Button(this);
        purchaseButton.setText("UNLOCK SACRED TABLE");
        purchaseButton.setEnabled(false);
        purchaseButton.setOnClickListener(v -> purchaseSacredTable());
        buttons.addView(purchaseButton, new LinearLayout.LayoutParams(
                0, ViewGroup.LayoutParams.WRAP_CONTENT, 1f));

        restoreButton = new Button(this);
        restoreButton.setText("RESTORE");
        restoreButton.setEnabled(false);
        restoreButton.setOnClickListener(v -> restorePurchases());
        buttons.addView(restoreButton, new LinearLayout.LayoutParams(
                0, ViewGroup.LayoutParams.WRAP_CONTENT, 1f));

        storeBar.addView(buttons);
        root.addView(storeBar);
        return root;
    }

    private void startGameServer() {
        new Thread(() -> {
            try {
                Python py = Python.getInstance();
                PyObject bridge = py.getModule("mobile_bridge");
                bridge.callAttr("start_server", GAME_PORT, 3);
                runOnUiThread(() -> webView.loadUrl(
                        "http://127.0.0.1:" + GAME_PORT + "/"));
            } catch (Exception error) {
                runOnUiThread(() -> purchaseStatus.setText(
                        "GAME START FAILED: " + error.getClass().getSimpleName()));
            }
        }, "politics-python-start").start();
    }

    private void configureRevenueCat() {
        String apiKey = BuildConfig.REVENUECAT_API_KEY;
        if (apiKey == null || apiKey.isEmpty()) {
            purchaseStatus.setText("SACRED TABLE: RevenueCat key not configured");
            return;
        }

        Purchases.configure(new PurchasesConfiguration.Builder(
                getApplicationContext(), apiKey).build());
        restoreButton.setEnabled(true);
        refreshCustomerInfo();
        loadOffering();
    }

    private void refreshCustomerInfo() {
        Purchases.getSharedInstance().getCustomerInfo(new ReceiveCustomerInfoCallback() {
            @Override
            public void onReceived(CustomerInfo customerInfo) {
                setOwnership(customerInfo);
            }

            @Override
            public void onError(PurchasesError error) {
                purchaseStatus.setText("SACRED TABLE: ownership unavailable");
            }
        });
    }

    private void loadOffering() {
        Purchases.getSharedInstance().getOfferings(new ReceiveOfferingsCallback() {
            @Override
            public void onReceived(Offerings offerings) {
                Offering current = offerings.getCurrent();
                List<Package> packages = current == null
                        ? null : current.getAvailablePackages();
                sacredTablePackage = (packages == null || packages.isEmpty())
                        ? null : packages.get(0);
                purchaseButton.setEnabled(!sacredTableOwned && sacredTablePackage != null);
                if (!sacredTableOwned && sacredTablePackage == null) {
                    purchaseStatus.setText("SACRED TABLE: configure a RevenueCat offering");
                }
            }

            @Override
            public void onError(PurchasesError error) {
                purchaseStatus.setText("SACRED TABLE: offering unavailable");
            }
        });
    }

    private void purchaseSacredTable() {
        if (sacredTablePackage == null || sacredTableOwned) {
            return;
        }
        purchaseButton.setEnabled(false);
        PurchaseParams params = new PurchaseParams.Builder(
                this, sacredTablePackage).build();
        Purchases.getSharedInstance().purchase(params, new PurchaseCallback() {
            @Override
            public void onCompleted(StoreTransaction storeTransaction,
                                    CustomerInfo customerInfo) {
                setOwnership(customerInfo);
            }

            @Override
            public void onError(PurchasesError error, boolean userCancelled) {
                if (userCancelled) {
                    purchaseStatus.setText("SACRED TABLE: purchase cancelled");
                } else {
                    purchaseStatus.setText("SACRED TABLE: purchase failed");
                }
                purchaseButton.setEnabled(sacredTablePackage != null);
            }
        });
    }

    private void restorePurchases() {
        restoreButton.setEnabled(false);
        Purchases.getSharedInstance().restorePurchases(new ReceiveCustomerInfoCallback() {
            @Override
            public void onReceived(CustomerInfo customerInfo) {
                restoreButton.setEnabled(true);
                setOwnership(customerInfo);
            }

            @Override
            public void onError(PurchasesError error) {
                restoreButton.setEnabled(true);
                purchaseStatus.setText("SACRED TABLE: restore failed");
            }
        });
    }

    private void setOwnership(CustomerInfo customerInfo) {
        EntitlementInfo entitlement = customerInfo.getEntitlements()
                .get(BuildConfig.REVENUECAT_ENTITLEMENT_ID);
        sacredTableOwned = entitlement != null && entitlement.isActive();
        if (sacredTableOwned) {
            purchaseStatus.setText("SACRED TABLE: owned permanently");
            purchaseButton.setText("SACRED TABLE OWNED");
            purchaseButton.setEnabled(false);
        } else {
            purchaseStatus.setText("SACRED TABLE: optional cosmetic unlock");
            purchaseButton.setText("UNLOCK SACRED TABLE");
            purchaseButton.setEnabled(sacredTablePackage != null);
        }
        applySacredTableSkin();
    }

    private void applySacredTableSkin() {
        if (webView == null || !sacredTableOwned) {
            return;
        }
        String js = "(() => {"
                + "document.body.style.background='#160d18';"
                + "document.body.style.color='#f1e8d2';"
                + "document.querySelectorAll('.card,.st').forEach(e=>{"
                + "e.style.borderColor='#b99b63';e.style.background='#201522';});"
                + "document.querySelectorAll('#tracks,#identity,#reaction').forEach(e=>"
                + "e.style.letterSpacing='0.04em');"
                + "})()";
        webView.evaluateJavascript(js, null);
    }

    @Override
    protected void onDestroy() {
        if (webView != null) {
            webView.destroy();
        }
        super.onDestroy();
    }
}
